import requests
from utils import get_user_agent
from decrypt import extract_from_html


def fetch_student_grades(student_id: str, cookies: dict) -> requests.Response:
    url = f"http://jwgl.sxzy.edu.cn/xscjcx.aspx?xh={student_id}"
    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "Referer": url,
        "User-Agent": get_user_agent()
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
