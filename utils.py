import re
import rsa
import hashlib
import time
from functools import wraps


def extract_from_html(pattern: str, html: str) -> str:
    match = re.search(pattern, html)
    return match.group(1) if match else None


def rsa_encrypt(plaintext: str, modulus: str) -> bytes:
    rsa_exponent = int('010001', 16)
    rsa_modulus = int(modulus, 16)
    public_key = rsa.PublicKey(n=rsa_modulus, e=rsa_exponent)
    return rsa.encrypt(plaintext.encode('utf-8'), public_key)


def bytes_to_hex_upper(data: bytes) -> str:
    return data.hex().upper()


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
                    print(f"重试第 {attempt + 1} 次失败，错误：{e}，等待 {delay} 秒后重试...")
                    time.sleep(delay)
            raise Exception(f"达到最大重试次数 {max_retries}，最后错误: {last_exception}")
        return wrapper
    return decorator


def retry(func, max_retries=3, delay=1):
    last_exception = None
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            print(f"重试第 {attempt + 1} 次失败，错误：{e}，等待 {delay} 秒后重试...")
            time.sleep(delay)
    raise Exception(f"自动重试达到最大次数：{max_retries}\n错误信息：{last_exception}")


def read_setting(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("ScoreUpdateReminder"):
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        raise Exception(f"未找到配置文件: {file_path}")
    except Exception as e:
        raise Exception(f"读取配置文件时出错: {e}")
    return "关闭"


def save_local(md_content: str, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(md_content)


def save_md5(md_content: str) -> str:
    return hashlib.md5(md_content.encode('utf-8')).hexdigest()


def get_user_agent() -> str:
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"


def build_login_data(username: str, password: str, rsa_modulus: str, verify_code: str) -> dict:
    return {
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
