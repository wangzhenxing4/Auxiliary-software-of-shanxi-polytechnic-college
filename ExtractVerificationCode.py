import ddddocr
from decrypt import extract_from_html


def get_verification_code_and_rsa_modulus(session) -> tuple[str, str]:
    """
    从登录页面获取验证码和 RSA 模数。

    参数:
    - session: requests.Session() 对象，用于发起 HTTP 请求。

    返回值:
    - 包含验证码和 RSA 模数的元组 (验证码, RSA 模数)。

    异常:
    - 如果无法提取验证码或 RSA 模数，则引发 ValueError。
    """
    # 设置请求头，模拟浏览器用户代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    }

    # 访问主页面以获取验证码和 RSA 模数
    response = session.get("http://jwgl.sxzy.edu.cn/", headers=headers)
    # 确保请求成功
    response.raise_for_status()

    # 从 HTML 内容中提取验证码的安全密钥和 RSA 模数
    verify_key = extract_from_html(r'src="/CheckCode.aspx\?SafeKey=([^"]+)"', response.text)
    rsa_modulus = extract_from_html(r'id="txtKeyModulus" style="display:none" value="([0-9A-F]+)"', response.text)

    # 检查是否成功提取了验证码和 RSA 模数
    if not verify_key or not rsa_modulus:
        raise ValueError("无法提取验证码或RSA模数")

    # 生成验证码图片的 URL
    verify_code_url = f"http://jwgl.sxzy.edu.cn/CheckCode.aspx?SafeKey={verify_key}"

    # 请求验证码图片
    picture_response = session.get(verify_code_url, headers=headers)
    # 确保请求成功
    picture_response.raise_for_status()

    # 使用 ddddocr 进行验证码识别
    verify_code = ddddocr.DdddOcr(show_ad=False).classification(picture_response.content)

    return verify_code, rsa_modulus
