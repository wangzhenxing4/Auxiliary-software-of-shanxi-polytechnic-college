import ddddocr
import requests
from utils import extract_from_html, get_user_agent, build_login_data


def get_verification_code_and_rsa_modulus(session) -> tuple[str, str]:
    headers = {"User-Agent": get_user_agent()}
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


def login_jwxt(username: str, password: str) -> tuple[requests.Session, str]:
    session = requests.Session()
    verify_code, rsa_modulus = get_verification_code_and_rsa_modulus(session)
    data = build_login_data(username, password, rsa_modulus, verify_code)
    headers = {"User-Agent": get_user_agent()}
    response = session.post("http://jwgl.sxzy.edu.cn/", headers=headers, data=data)
    response.raise_for_status()
    full_name = extract_student_names(response)
    return session, full_name


def fetch_id_card_number(session: requests.Session, student_id: str) -> str:
    url = f"http://jwgl.sxzy.edu.cn/xsgrxx.aspx?xh={student_id}"
    headers = {"User-Agent": get_user_agent(), "Referer": f"http://jwgl.sxzy.edu.cn/xs_main.aspx?xh={student_id}"}
    response = session.get(url, headers=headers, allow_redirects=False)
    response.raise_for_status()
    html_content = response.text
    id_card_number = extract_from_html(r'<span id="lbl_sfzh">([^<]+)</span>', html_content)
    if not id_card_number:
        raise ValueError("无法提取身份证号码")
    return id_card_number


def extract_student_names(response: requests.Response) -> str:
    html_content = response.text
    full_name = extract_from_html(r'<span id="xhxm">([^<]+)同学</span>', html_content)
    if not full_name:
        raise ValueError("无法提取学生姓名")
    return full_name
