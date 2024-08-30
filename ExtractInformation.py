import urllib.parse
import requests
from utils import get_user_agent
from decrypt import extract_from_html


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


def get_name(cookies) -> str:
    if 'unm' in cookies:
        unm = cookies['unm']
        return urllib.parse.unquote(unm)
    else:
        raise Exception("无法获取到打卡人的姓名")
