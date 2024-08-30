import requests
from utils import get_user_agent
from decrypt import extract_from_html


def fetch_student_grades(student_id: str, cookies: dict) -> requests.Response:
    """
    获取学生的成绩信息。

    参数:
    - student_id: 学生的学号。
    - cookies: 包含登录信息的 cookies，用于访问成绩页面。

    返回值:
    - 返回包含成绩信息的 HTTP 响应对象。

    异常:
    - 如果无法从 HTML 中提取 viewstate 或 eventvalidation，抛出 ValueError。
    """
    # 设置成绩查询页面的 URL
    url = f"http://jwgl.sxzy.edu.cn/xscjcx.aspx?xh={student_id}"

    # 设置请求头，包括 cookies 和用户代理
    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "Referer": url,
        "User-Agent": get_user_agent()
    }

    # 发送 GET 请求以获取成绩查询页面
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 如果请求失败，抛出 HTTPError

    # 从 HTML 内容中提取 viewstate 和 eventvalidation 值
    html_content = response.text
    viewstate = extract_from_html(r'id="__VIEWSTATE" value="([^"]+)"', html_content)
    eventvalidation = extract_from_html(r'id="__EVENTVALIDATION" value="([^"]+)"', html_content)

    # 如果提取失败，则抛出 ValueError
    if not viewstate or not eventvalidation:
        raise ValueError("无法获取成绩")

    # 准备提交的数据
    data = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": eventvalidation,
        "ddlXN": "2023-2024",  # 学年，示例值
        "ddlXQ": "2",  # 学期，示例值
        "btn_xq": "学期成绩"  # 按钮值
    }

    # 发送 POST 请求以提交成绩查询表单
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # 如果请求失败，抛出 HTTPError

    return response
