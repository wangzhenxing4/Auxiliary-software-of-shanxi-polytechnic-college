import urllib.parse
import requests
from utils import get_user_agent
from decrypt import extract_from_html


def fetch_id_card_number(session: requests.Session, student_id: str) -> str:
    """
    从学校的系统页面中提取学生的身份证号码。

    参数:
    - session: requests.Session() 对象，用于发起请求。
    - student_id: 学生的学号。

    返回值:
    - 学生的身份证号码。

    异常:
    - 如果无法提取身份证号码，则引发 ValueError。
    """
    # 生成请求 URL
    url = f"http://jwgl.sxzy.edu.cn/xsgrxx.aspx?xh={student_id}"

    # 设置请求头
    headers = {
        "User-Agent": get_user_agent(),
        "Referer": f"http://jwgl.sxzy.edu.cn/xs_main.aspx?xh={student_id}"
    }

    # 发起 GET 请求
    response = session.get(url, headers=headers, allow_redirects=False)
    # 确保请求成功
    response.raise_for_status()

    # 获取响应的 HTML 内容
    html_content = response.text

    # 从 HTML 内容中提取身份证号码
    id_card_number = extract_from_html(r'<span id="lbl_sfzh">([^<]+)</span>', html_content)

    if not id_card_number:
        raise ValueError("无法提取身份证号码")

    return id_card_number


def extract_student_names(response: requests.Response) -> str:
    """
    从响应中提取学生的全名。

    参数:
    - response: requests.Response 对象，包含学生信息的 HTML 内容。

    返回值:
    - 学生的全名。

    异常:
    - 如果无法提取学生姓名，则引发 ValueError。
    """
    # 获取响应的 HTML 内容
    html_content = response.text

    # 从 HTML 内容中提取学生的全名
    full_name = extract_from_html(r'<span id="xhxm">([^<]+)同学</span>', html_content)

    if not full_name:
        raise ValueError("无法提取学生姓名")

    return full_name


def get_name(cookies) -> str:
    """
    从 cookies 中提取打卡人的姓名。

    参数:
    - cookies: 包含 cookies 的字典。

    返回值:
    - 打卡人的姓名。

    异常:
    - 如果无法从 cookies 中提取姓名，则引发 Exception。
    """
    if 'unm' in cookies:
        unm = cookies['unm']
        return urllib.parse.unquote(unm)  # 解码 URL 编码的姓名
    else:
        raise Exception("无法获取到打卡人的姓名")
