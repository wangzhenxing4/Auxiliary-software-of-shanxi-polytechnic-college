import urllib.parse
import requests
from utils import get_user_agent
from decrypt import extract_from_html


def fetch_id_card_number(session: requests.Session, student_id: str) -> str:
    """
    从教务系统获取学生的身份证号码

    参数:
    session (requests.Session): 已经建立的会话对象，用于发送 HTTP 请求
    student_id (str): 学生的学号

    返回:
    str: 学生的身份证号码

    异常:
    ValueError: 如果无法从响应中提取身份证号码
    """
    # 构造请求 URL
    url = f"http://jwgl.sxzy.edu.cn/xsgrxx.aspx?xh={student_id}"

    # 设置请求头
    headers = {
        "User-Agent": get_user_agent(),
        "Referer": f"http://jwgl.sxzy.edu.cn/xs_main.aspx?xh={student_id}"
    }

    # 发送 GET 请求获取学生个人信息页面
    response = session.get(url, headers=headers, allow_redirects=False)
    response.raise_for_status()  # 检查请求是否成功

    # 提取页面内容
    html_content = response.text

    # 从 HTML 内容中提取身份证号码
    id_card_number = extract_from_html(r'<span id="lbl_sfzh">([^<]+)</span>', html_content)

    # 如果无法提取身份证号码，则抛出异常
    if not id_card_number:
        raise ValueError("无法提取身份证号码")

    return id_card_number


def extract_student_names(response: requests.Response) -> str:
    """
    从教务系统的响应中提取学生姓名

    参数:
    response (requests.Response): 包含学生信息的 HTTP 响应对象

    返回:
    str: 学生的全名

    异常:
    ValueError: 如果无法从响应中提取学生姓名
    """
    # 提取页面内容
    html_content = response.text

    # 从 HTML 内容中提取学生姓名
    full_name = extract_from_html(r'<span id="xhxm">([^<]+)同学</span>', html_content)

    # 如果无法提取学生姓名，则抛出异常
    if not full_name:
        raise ValueError("无法提取学生姓名")

    return full_name


def get_name(cookies) -> str:
    """
    从 Cookies 中获取打卡人的姓名

    参数:
    cookies (dict): 包含打卡人姓名的 Cookies

    返回:
    str: 打卡人的姓名

    异常:
    Exception: 如果 Cookies 中无法找到打卡人的姓名
    """
    # 检查 Cookies 中是否包含 'unm' 键
    if 'unm' in cookies:
        unm = cookies['unm']
        # URL 解码姓名
        return urllib.parse.unquote(unm)
    else:
        raise Exception("无法获取到打卡人的姓名")
