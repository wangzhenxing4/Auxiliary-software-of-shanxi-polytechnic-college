import re
import rsa


def bytes_to_hex_upper(data: bytes) -> str:
    """
    将字节数据转换为大写的十六进制字符串

    参数:
    data (bytes): 要转换的字节数据

    返回:
    str: 对应的大写十六进制字符串
    """
    return data.hex().upper()


def extract_from_html(pattern: str, html: str) -> str:
    """
    从 HTML 文本中提取符合模式的字符串

    参数:
    pattern (str): 用于匹配的正则表达式模式
    html (str): 包含 HTML 内容的字符串

    返回:
    str: 匹配到的字符串，如果没有匹配则返回 None
    """
    match = re.search(pattern, html)
    return match.group(1) if match else None


def rsa_encrypt(plaintext: str, modulus: str) -> bytes:
    """
    使用 RSA 加密算法对明文进行加密

    参数:
    plaintext (str): 要加密的明文字符串
    modulus (str): RSA 公钥模数（十六进制字符串）

    返回:
    bytes: 加密后的字节数据
    """
    rsa_exponent = int('010001', 16)    # RSA 公钥指数，通常为 65537（0x10001）
    rsa_modulus = int(modulus, 16)  # 将十六进制字符串转换为整数
    public_key = rsa.PublicKey(n=rsa_modulus, e=rsa_exponent)   # 创建 RSA 公钥对象
    return rsa.encrypt(plaintext.encode('utf-8'), public_key)   # 对明文进行加密并返回加密结果
