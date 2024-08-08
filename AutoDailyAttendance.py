import os
import requests
import urllib.parse
import random
from time import sleep
import re
import ddddocr
import rsa
from bs4 import BeautifulSoup
from functools import wraps


student_id = os.environ.get("STUDENT_ID")
password = os.environ.get("PASSWORD")
check_in_address_school = os.environ.get("SCHOOL_ADDRESS")
check_in_address_home = os.environ.get("HOLIDAY_ADDRESS")
token = os.environ.get("PUSH_MESSAGE_TOKEN")
CHECK_IN_TIME = '放假'


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
        raise ValueError("无法提取验证码或RSA模数")
    verify_code_url = f"http://jwgl.sxzy.edu.cn/CheckCode.aspx?SafeKey={verify_key}"
    picture_response = session.get(verify_code_url, headers=headers)
    picture_response.raise_for_status()
    verify_code = ddddocr.DdddOcr(show_ad=False).classification(picture_response.content)
    return verify_code, rsa_modulus


def retry_on_exception(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"尝试第 {attempt + 1} 次失败: {e}")
                    sleep(delay)
            raise Exception(f"达到最大重试次数 {max_retries}，最后错误: {last_exception}")
        return wrapper
    return decorator


@retry_on_exception(max_retries=3, delay=2)
def login_jwxt(username: str, password: str) -> requests.Session:
    session = requests.Session()
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
    return session


@retry_on_exception(max_retries=3, delay=2)
def fetch_id_card_number(session: requests.Session, student_id: str) -> str:
    url = f"http://jwgl.sxzy.edu.cn/xsgrxx.aspx?xh={student_id}&xm=王振兴&gnmkdm=N121501"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
        "Referer": f"http://jwgl.sxzy.edu.cn/xs_main.aspx?xh={student_id}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Connection": "keep-alive"
    }
    response = session.get(url, headers=headers, allow_redirects=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    id_card_tag = soup.find('span', id='lbl_sfzh')
    if id_card_tag:
        id_card_number_of_punch_in_person = id_card_tag.get_text().strip()
    else:
        raise ValueError("无法提取身份证号码")
    return id_card_number_of_punch_in_person


def read_setting(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("AutoDailyAttendance"):
                return line.split('=')[1].strip()
    return None


def retry(func, max_retries=3, delay=1):
    last_exception = None
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            print(f"自动尝试重试，第{attempt + 1}次：{e}")
            sleep(delay)
    raise Exception(f"自动重试达到最大次数：{max_retries}\n错误信息：{last_exception}")


def setup():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; Redmi K30i 5G Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.120 Mobile Safari/537.36 XWEB/1220099 MMWEBSDK/20240404 MMWEBID/5158 MicroMessenger/8.0.49.2600(0x28003154) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Referer": "http://fdcat.cn365vip.com/index103.php?code=0314LBll2jCZHd4cpTol2klxUR14LBlu&state=1"
    }
    login_url = "http://fdcat.cn365vip.com/addu.php"
    response = session.post(login_url, data={"u_name": id_card_number_of_punch_in_person, "upwd": "111111"}, headers=headers)
    response.raise_for_status()
    cookies = session.cookies.get_dict()
    name_of_clock_in_personnel = get_name(cookies)
    return session, headers, name_of_clock_in_personnel


def get_name(cookies):
    if 'unm' in cookies:
        unm = cookies['unm']
        return urllib.parse.unquote(unm)
    else:
        raise Exception("无法获取到打卡人的姓名")


def main():
    setting_file_path = "Switch"
    auto_daily_attendance = read_setting(setting_file_path)
    if auto_daily_attendance == "关闭":
        print("自动打卡已关闭")
        return

    session, headers, name_of_clock_in_personnel = setup()
    results = []
    try:
        retry(lambda: login(session, id_card_number_of_punch_in_person, headers))
        temperature, check_in_address = retry(
            lambda: checkin(session, name_of_clock_in_personnel, check_in_address_school, check_in_address_home, headers))
        results.append((name_of_clock_in_personnel, "的自动打卡已成功", f"打卡温度：36.{temperature}，打卡地点：{check_in_address}"))
        push_notification(token, f"**{name_of_clock_in_personnel}的自动打卡执行成功**\n打卡温度：36.{temperature}，打卡地点：{check_in_address}", name_of_clock_in_personnel, success=True)
    except Exception as e:
        results.append((name_of_clock_in_personnel, f"错误原因：{e}"))
        print(f"自动打卡失败：{e}")
        push_notification(token, f"自动打卡失败\n错误原因：{e}", name_of_clock_in_personnel, success=False)
    finally:
        session.close()
    return results


def login(session, id_card_number_of_punch_in_person, headers):
    login_url = "http://fdcat.cn365vip.com/addu.php"
    response = session.post(login_url, data={"u_name": id_card_number_of_punch_in_person, "upwd": "111111"}, headers=headers)
    response.raise_for_status()


def checkin(session, name_of_clock_in_personnel, check_in_address_school, check_in_address_home, headers):
    checkin_url = "http://fdcat.cn365vip.com/adddt_s2_up.php"
    check_in_address = check_in_address_home if CHECK_IN_TIME == '放假' else check_in_address_school
    temperature = str(random.randint(0, 9))
    payload = {
        "u_addr": check_in_address,
        "vname": name_of_clock_in_personnel,
        "tw1": "36",
        "tw2": temperature,
    }
    response = session.post(checkin_url, data=payload, headers=headers)
    response.raise_for_status()
    return temperature, check_in_address


def push_notification(url, content, name_of_clock_in_personnel, success):
    if not url:
        return
    title = f"{name_of_clock_in_personnel}的自动打卡执行成功" if success else f"**{name_of_clock_in_personnel}的自动打卡执行失败**"
    data = {
        "title": title,
        "content": content,
        "template": "html"
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"推送失败：{e}")


if __name__ == "__main__":
    session = login_jwxt(student_id, password)
    id_card_number_of_punch_in_person = fetch_id_card_number(session, student_id)
    main()
