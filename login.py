import requests
from ExtractInformation import extract_student_names
from ExtractVerificationCode import get_verification_code_and_rsa_modulus
from decrypt import rsa_encrypt, bytes_to_hex_upper
from utils import get_user_agent
from retry import retry


def build_login_data(username: str, password: str, rsa_modulus: str, verify_code: str) -> dict:
    """
    构建登录请求的数据

    参数:
    username (str): 用户名
    password (str): 密码
    rsa_modulus (str): RSA 模数
    verify_code (str): 验证码

    返回:
    dict: 构建的登录数据
    """
    return {
        "__VIEWSTATE": "tA6uBVKFegpyqnoAaHndgJpnE5COnAaCgoHV7Y3HhVb5hEH5WAjqds6F6l4ABOPYbAgvkGL8voLxZe/bkFq2R2ka+8A=",
        "__VIEWSTATEGENERATOR": "0564CA07",
        "__EVENTVALIDATION": "sn2KJ9wlNDzVvr5WZDL+uxBk4M4Wj8jgLjEjaxvHD/AYIXku5dH3FOT0SYvQ72EVlnwAQpApuHY7rcjdnwOhv"
                             "+BfNVjsDU+6LmqP0gG202suxNXXVCnDhsb5NKaurjmy6OVJqflrgAS3ZMX2ujXhFBO3ftr9sPeagR2VPoF2zDZ0"
                             "/1+9xn6yDPSWUYlnr8bgIGXbWvo2ykEr4C8/qOuNK"
                             "+tCJVrbt7r7FaSbFJdM5zgJaK7GqqZeRwRyIuMgZC1cZt0tXZ1ze6Sz3XxuTeBokkYGfxkdslj5yc1dTscLMcLQGz4Y6M0Uh0RHHaHfKO+BbJnUzxkdjpNSdASh8uV2jnP8smI=",
        "TextBox1": username,  # 用户名字段
        "TextBox2": bytes_to_hex_upper(rsa_encrypt(password, rsa_modulus)),  # 加密后的密码字段
        "txtSecretCode": verify_code,  # 验证码字段
        "RadioButtonList1": "学生",  # 角色选择，默认选择学生
        "Button1": "登录",  # 登录按钮
        "txtKeyExponent": "010001",  # RSA 公钥指数
        "txtKeyModulus": rsa_modulus,  # RSA 公钥模数
    }


@retry(stop_exceptions=(ValueError,))
def login_jwxt_ttdk(username: str, password: str) -> requests.Session:
    """
    使用用户名和密码登录教务系统并返回会话对象

    参数:
    username (str): 用户名
    password (str): 密码

    返回:
    requests.Session: 登录后的会话对象

    异常:
    ValueError: 如果密码错误
    Exception: 如果验证码不正确
    """
    session = requests.Session()  # 创建一个会话对象
    verify_code, rsa_modulus = get_verification_code_and_rsa_modulus(session)  # 获取验证码和 RSA 模数
    data = build_login_data(username, password, rsa_modulus, verify_code)  # 构建登录数据
    headers = {"User-Agent": get_user_agent()}  # 设置请求头
    response = session.post("http://jwgl.sxzy.edu.cn/", headers=headers, data=data)  # 发送 POST 请求登录
    response.raise_for_status()  # 检查请求是否成功
    if "密码错误" in response.text:  # 检查登录失败原因
        raise ValueError("登录失败：密码错误，程序终止！")
    if "验证码不正确！！" in response.text:
        raise Exception("验证码不正确！！")
    return session


@retry(stop_exceptions=(ValueError,))
def login_jwxt(username: str, password: str) -> tuple:
    """
    使用用户名和密码登录教务系统并返回会话对象及全名

    参数:
    username (str): 用户名
    password (str): 密码

    返回:
    tuple: 包含会话对象和用户全名的元组

    异常:
    ValueError: 如果密码错误
    Exception: 如果验证码不正确
    """
    session = requests.Session()  # 创建一个会话对象
    verify_code, rsa_modulus = get_verification_code_and_rsa_modulus(session)  # 获取验证码和 RSA 模数
    data = build_login_data(username, password, rsa_modulus, verify_code)  # 构建登录数据
    headers = {"User-Agent": get_user_agent()}  # 设置请求头
    response = session.post("http://jwgl.sxzy.edu.cn/", headers=headers, data=data)  # 发送 POST 请求登录
    response.raise_for_status()  # 检查请求是否成功
    if "密码错误" in response.text:  # 检查登录失败原因
        raise ValueError("登录失败：密码错误，程序终止！")
    if "验证码不正确！！" in response.text:
        raise Exception("验证码不正确！！")
    full_name = extract_student_names(response)  # 从响应中提取学生全名
    return session, full_name
