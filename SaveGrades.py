import hashlib
from notification import score_information_push


def save(md_content: str, full_name: str, push_token: str) -> None:
    """
    保存成绩信息并根据内容变化发送推送通知。

    参数:
    - md_content: 要保存的成绩内容（Markdown 格式）。
    - full_name: 学生的全名。
    - push_token: 推送通知的 token。

    异常:
    - 如果内容为空，抛出 ValueError。
    """
    if not md_content.strip():
        raise ValueError("内容获取失败")

    old_filename = f"{full_name}成绩.md"
    md5_filename = 'md_content.txt'
    new_md5 = save_md5(md_content)

    try:
        with open(md5_filename, 'r', encoding='utf-8') as file:
            old_md5 = file.read().strip()
    except FileNotFoundError:
        old_md5 = ""

    if new_md5 == old_md5:
        print("成绩没有更新")
        return

    # 保存成绩内容到文件
    save_local(md_content, old_filename)

    # 更新 MD5 文件
    with open(md5_filename, 'w', encoding='utf-8') as file:
        file.write(new_md5)

    # 标记 MD5 发生变化
    with open('push_flag.txt', 'w') as file:
        file.write('MD5 changed')

    # 发送推送通知
    score_information_push(md_content, full_name, push_token, success=True)


def save_local(md_content: str, filename: str) -> None:
    """
    将内容保存到本地文件。

    参数:
    - md_content: 要保存的内容（Markdown 格式）。
    - filename: 文件名。
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(md_content)


def save_md5(md_content: str) -> str:
    """
    计算并返回内容的 MD5 哈希值。

    参数:
    - md_content: 要计算 MD5 哈希的内容。

    返回值:
    - 内容的 MD5 哈希值（十六进制字符串）。
    """
    return hashlib.md5(md_content.encode('utf-8')).hexdigest()
