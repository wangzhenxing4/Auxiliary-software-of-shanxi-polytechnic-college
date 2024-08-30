import re
import rsa

def bytes_to_hex_upper(data: bytes) -> str:
    """
    将字节数据转换为大写的十六进制字符串。

    参数:
    - data: 要转换的字节数据。

    返回值:
    - 以大写形式表示的十六进制字符串。
    """
    return data.hex().upper()

def extract_from_html(pattern: str, html: str) -> str:
    """
    从 HTML 内容中提取符合正则表达式模式的第一个匹配组。

    参数:
    - pattern: 用于匹配的正则表达式模式。
    - html: 需要提取数据的 HTML 字符串。

    返回值:
    - 如果找到匹配项，则返回第一个匹配组的内容；否则返回 None。
    """
    match = re.search(pattern, html)
    return match.group(1) if match else None

def rsa_encrypt(plaintext: str, modulus: str) -> bytes:
    """
    使用 RSA 公钥对明文进行加密。

    参数:
    - plaintext: 要加密的明文字符串。
    - modulus: RSA 公钥的模数，以十六进制字符串形式表示。

    返回值:
    - 加密后的字节数据。
    """
    rsa_exponent = int('010001', 16)  # RSA 公钥的指数（常见的 65537）
    rsa_modulus = int(modulus, 16)  # 从十六进制字符串转换为整数的模数
    public_key = rsa.PublicKey(n=rsa_modulus, e=rsa_exponent)  # 创建 RSA 公钥对象
    return rsa.encrypt(plaintext.encode('utf-8'), public_key)  # 加密明文并返回字节数据
