import re
import rsa


def bytes_to_hex_upper(data: bytes) -> str:
    return data.hex().upper()


def extract_from_html(pattern: str, html: str) -> str:
    match = re.search(pattern, html)
    return match.group(1) if match else None


def rsa_encrypt(plaintext: str, modulus: str) -> bytes:
    rsa_exponent = int('010001', 16)
    rsa_modulus = int(modulus, 16)
    public_key = rsa.PublicKey(n=rsa_modulus, e=rsa_exponent)
    return rsa.encrypt(plaintext.encode('utf-8'), public_key)

