import ddddocr
from decrypt import extract_from_html


def get_verification_code_and_rsa_modulus(session) -> tuple[str, str]:
    """
    获取验证码和 RSA 模数

    参数:
    session (requests.Session): 已经建立的会话对象，用于发送 HTTP 请求

    返回:
    tuple: 包含验证码和 RSA 模数的元组 (verify_code, rsa_modulus)

    异常:
    ValueError: 如果无法提取验证码或 RSA 模数
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    }

    # 发送 GET 请求获取初始页面
    response = session.get("http://jwgl.sxzy.edu.cn/", headers=headers)
    response.raise_for_status()  # 检查请求是否成功

    # 从 HTML 内容中提取验证码的 SafeKey 和 RSA 模数
    verify_key = extract_from_html(r'src="/CheckCode.aspx\?SafeKey=([^"]+)"', response.text)
    rsa_modulus = extract_from_html(r'id="txtKeyModulus" style="display:none" value="([0-9A-F]+)"', response.text)

    # 如果无法提取所需信息，则抛出异常
    if not verify_key or not rsa_modulus:
        raise ValueError("无法提取验证码或RSA模数")

    # 构造验证码图片的 URL 并发送 GET 请求获取图片内容
    verify_code_url = f"http://jwgl.sxzy.edu.cn/CheckCode.aspx?SafeKey={verify_key}"
    picture_response = session.get(verify_code_url, headers=headers)
    picture_response.raise_for_status()  # 检查请求是否成功

    # 使用 ddddocr 库对验证码图片进行识别
    verify_code = ddddocr.DdddOcr(show_ad=False).classification(picture_response.content)

    return verify_code, rsa_modulus
