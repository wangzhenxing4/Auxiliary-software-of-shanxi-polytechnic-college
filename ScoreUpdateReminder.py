import re
import ddddocr
import requests
import rsa
import os
import hashlib


student_id = os.environ.get("STUDENT_ID")
password = os.environ.get("PASSWORD")
token = os.environ.get("PUSH_MESSAGE_TOKEN")


def bytes_to_hex_upper(data: bytes) -> str:
    return data.hex().upper()


def extract_from_html(pattern: str, html: str) -> str:
    match = re.search(pattern, html)
    return match.group(1) if match else None


def rsa_encrypt(plaintext: str, modulus: str) -> bytes:
    rsa_exponent = int('010001', 16)
    rsa_modulus = int(modulus, 16)
    public_key = rsa.PublicKey(n=rsa_modulus, e=rsa_exponent)
    return rsa.encrypt(plaintext.encode('utf-8'), public_key)


def get_verification_code_and_rsa_modulus(session) -> tuple[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    }
    response = session.get("http://jwgl.sxzy.edu.cn/", headers=headers)
    response.raise_for_status()
    verify_key = extract_from_html(r'src="/CheckCode.aspx\?SafeKey=([^"]+)"', response.text)
    rsa_modulus = extract_from_html(r'id="txtKeyModulus" style="display:none" value="([0-9A-F]+)"', response.text)
    if not verify_key or not rsa_modulus:
        raise ValueError("无法提取验证码")
    verify_code_url = f"http://jwgl.sxzy.edu.cn/CheckCode.aspx?SafeKey={verify_key}"
    picture_response = session.get(verify_code_url, headers=headers)
    picture_response.raise_for_status()
    verify_code = ddddocr.DdddOcr(show_ad=False).classification(picture_response.content)
    return verify_code, rsa_modulus

def read_setting(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("ScoreUpdateReminder"):
                return line.split('=')[1].strip()
    return None


def login(username: str, password: str) -> tuple[dict, str]:
    with requests.Session() as session:
        verify_code, rsa_modulus = get_verification_code_and_rsa_modulus(session)
        data = {
            "__VIEWSTATE": "tA6uBVKFegpyqnoAaHndgJpnE5COnAaCgoHV7Y3HhVb5hEH5WAjqds6F6l4ABOPYbAgvkGL8voLxZe/bkFq2R2ka+8A=",
            "__VIEWSTATEGENERATOR": "0564CA07",
            "__EVENTVALIDATION": "sn2KJ9wlNDzVvr5WZDL+uxBk4M4Wj8jgLjEjaxvHD/AYIXku5dH3FOT0SYvQ72EVlnwAQpApuHY7rcjdnwOhv"
                                 "+BfNVjsDU+6LmqP0gG202suxNXXVCnDhsb5NKaurjmy6OVJqflrgAS3ZMX2ujXhFBO3ftr9sPeagR2VPoF2zDZ0"
                                 "/1+9xn6yDPSWUYlnr8bgIGXbWvo2ykEr4C8/qOuNK"
                                 "+tCJVrbt7r7FaSbFJdM5zgJaK7GqqZeRwRyIuMgZC1cZt0tXZ1ze6Sz3XxuTeBokkYGfxkdslj5yc1dTscLMcLQGz4Y6M0Uh0RHHaHfKO+BbJnUzxkdjpNSdASh8uV2jnP8smI=",
            "TextBox1": username,
            "TextBox2": bytes_to_hex_upper(rsa_encrypt(password, rsa_modulus)),
            "txtSecretCode": verify_code,
            "RadioButtonList1": "学生",
            "Button1": "登录",
            "txtKeyExponent": "010001",
            "txtKeyModulus": rsa_modulus,
        }
        headers = {
            "User-Agent": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        }
        response = session.post("http://jwgl.sxzy.edu.cn/", headers=headers, data=data)
        response.raise_for_status()
        full_name = extract_student_names(response)
        return session.cookies.get_dict(), full_name


def extract_student_names(response: requests.Response) -> str:
    html_content = response.text
    full_name = extract_from_html(r'<span id="xhxm">([^<]+)同学</span>', html_content)
    if not full_name:
        raise ValueError("无法提取学生姓名")
    return full_name


def fetch_student_grades(student_id: str, cookies: dict) -> requests.Response:
    url = f"http://jwgl.sxzy.edu.cn/xscjcx.aspx?xh={student_id}"
    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text
    viewstate = extract_from_html(r'id="__VIEWSTATE" value="([^"]+)"', html_content)
    eventvalidation = extract_from_html(r'id="__EVENTVALIDATION" value="([^"]+)"', html_content)
    if not viewstate or not eventvalidation:
        raise ValueError("无法获取成绩")
    data = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": eventvalidation,
        "ddlXN": "2023-2024",
        "ddlXQ": "2",
        "btn_xq": "学期成绩"
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response


def extract_grades(response: requests.Response) -> str:
    html_content = response.text
    pattern = re.compile(
        r'<tr(?: class="alt")?>\s*<td>(?P<year>\d{4}-\d{4})</td>\s*<td>(?P<term>\d)</td>\s*<td>(?P<course_code>\d+)</td>\s*<td>(?P<course_name>.*?)</td>\s*<td>(?P<course_nature>.*?)</td>\s*<td>(?P<course_affiliation>&nbsp;|.*?)</td>\s*<td>(?P<credit>[\d.]+)</td>\s*<td>(?P<grade_point>[\d.]+)</td>\s*<td>(?P<score>[\d.]+|优秀|良好|及格|不及格)</td>\s*<td>(?P<minor_flag>\d+)</td>\s*<td>(?P<makeup_score>&nbsp;|.*?)</td>\s*<td>(?P<retake_score>&nbsp;|.*?)</td>\s*<td>(?P<teaching_department>.*?)</td>\s*<td>(?P<remark>.*?)</td>\s*<td>(?P<retake_flag>.*?)</td>\s*</tr>'
    )
    matches = pattern.findall(html_content)
    score_summary = []
    for match in matches:
        course_info = {
            "学年": match[0],
            "学期": match[1],
            "课程代号": match[2],
            "课程名称": match[3],
            "课程性质": match[4],
            "学分": match[6],
            "绩点": match[7],
            "成绩": match[8],
            "开设学院": match[12]
        }
        score_summary.append(course_info)

    md_content = "\n\n".join(
        f"### 课程名称: {course['课程名称']}\n"
        f"- **课程性质**: {course['课程性质']}\n"
        f"- **学年**: {course['学年']}\n"
        f"- **学期**: {course['学期']}\n"
        f"- **课程代码**: {course['课程代号']}\n"
        f"- **学分**: {course['学分']}\n"
        f"- **绩点**: {course['绩点']}\n"
        f"- **成绩**: {course['成绩']}\n"
        f"- **开设学院**: {course['开设学院']}"
        for course in score_summary
    )
    return md_content


def save_local(md_content: str, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(md_content)


def save_md5(md_content: str) -> str:
    return hashlib.md5(md_content.encode('utf-8')).hexdigest()


def save(md_content: str, full_name: str, push_token: str):
    if not md_content.strip():
        raise ValueError("内容获取失败")

    old_filename = "成绩.md"
    md5_filename = 'md_content.txt'
    new_md5 = save_md5(md_content)

    try:
        with open(md5_filename, 'r', encoding='utf-8') as file:
            old_md5 = file.read().strip()
    except FileNotFoundError:
        old_md5 = ""

    if new_md5 == old_md5:
        print("成绩没有更新")
    else:
        push_service(md_content, full_name, push_token)
        save_local(md_content, old_filename)
        with open(md5_filename, 'w', encoding='utf-8') as file:
            file.write(new_md5)
        with open('push_flag.txt', 'w') as file:
            file.write('MD5 changed')


def rerun(max_retries=5):
    setting_file_path = "Switch"
    score_update_reminder = read_setting(setting_file_path)
    if score_update_reminder == "关闭":
        print("成绩更新提醒已关闭。")
        return

    global student_id, password, token

    personnel_data = [(student_id, password, token)]

    for student_id, password, push_token in personnel_data:
        attempt = 0
        while attempt < max_retries:
            try:
                cookies, full_name = login(student_id, password)
                response = fetch_student_grades(student_id, cookies)
                md_content = extract_grades(response)
                save(md_content, full_name, push_token)
                break
            except ValueError as e:
                print(e)
                attempt += 1
                if attempt >= max_retries:
                    print(f"达到最大重试次数，程序终止。")
                    break


def push_service(md_content: str, full_name: str, push_token: str):
    url = f"{push_token}"
    data = {
        "title": f"{full_name}考试成绩推送",
        "content": md_content,
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"推送失败：{e}")


if __name__ == "__main__":
    rerun()
