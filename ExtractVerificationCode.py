import ddddocr
from decrypt import extract_from_html


def get_verification_code_and_rsa_modulus(session) -> tuple[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    }
    response = session.get("http://jwgl.sxzy.edu.cn/", headers=headers)
    response.raise_for_status()
    verify_key = extract_from_html(r'src="/CheckCode.aspx\?SafeKey=([^"]+)"', response.text)
    rsa_modulus = extract_from_html(r'id="txtKeyModulus" style="display:none" value="([0-9A-F]+)"', response.text)
    if not verify_key or not rsa_modulus:
        raise ValueError("无法提取验证码或RSA模数")
    verify_code_url = f"http://jwgl.sxzy.edu.cn/CheckCode.aspx?SafeKey={verify_key}"
    picture_response = session.get(verify_code_url, headers=headers)
    picture_response.raise_for_status()
    verify_code = ddddocr.DdddOcr(show_ad=False).classification(picture_response.content)
    return verify_code, rsa_modulus
