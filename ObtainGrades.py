import requests
from utils import get_user_agent
from decrypt import extract_from_html


def fetch_student_grades(student_id: str, cookies: dict) -> requests.Response:
    """
    获取学生成绩的 HTTP 响应

    参数:
    student_id (str): 学生的学号
    cookies (dict): 请求所需的 Cookies

    返回:
    requests.Response: 包含学生成绩的 HTTP 响应对象

    异常:
    ValueError: 如果无法从页面中提取必要的信息
    """
    # 构造成绩查询的 URL
    url = f"http://jwgl.sxzy.edu.cn/xscjcx.aspx?xh={student_id}"

    # 构造 HTTP 请求头
    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "Referer": url,
        "User-Agent": get_user_agent()
    }

    # 发送 GET 请求以获取成绩页面
    response = requests.get(url, headers=headers)
    # 检查请求是否成功
    response.raise_for_status()
    html_content = response.text

    # 从 HTML 内容中提取 __VIEWSTATE 和 __EVENTVALIDATION 值
    viewstate = extract_from_html(r'id="__VIEWSTATE" value="([^"]+)"', html_content)
    eventvalidation = extract_from_html(r'id="__EVENTVALIDATION" value="([^"]+)"', html_content)

    # 如果无法获取 viewstate 或 eventvalidation，抛出异常
    if not viewstate or not eventvalidation:
        raise ValueError("无法获取成绩")

    # 构造 POST 请求所需的数据
    data = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": eventvalidation,
        "ddlXN": "2023-2024",  # 学年
        "ddlXQ": "2",  # 学期
        "btn_xq": "学期成绩"  # 按钮名称
    }

    # 发送 POST 请求以获取成绩
    response = requests.post(url, headers=headers, data=data)
    # 检查请求是否成功
    response.raise_for_status()
    return response
