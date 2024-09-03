import hashlib
from notification import score_information_push


def save(md_content: str, full_name: str, push_token: str):
    # 检查内容是否为空，如果为空则抛出 ValueError 异常
    if not md_content.strip():
        raise ValueError("内容获取失败")

    # 定义旧的文件名和保存 MD5 值的文件名
    old_filename = f"{full_name}成绩.md"
    md5_filename = 'md_content.txt'

    # 计算新内容的 MD5 值
    new_md5 = save_md5(md_content)

    try:
        # 尝试读取存储的旧 MD5 值
        with open(md5_filename, 'r', encoding='utf-8') as file:
            old_md5 = file.read().strip()
    except FileNotFoundError:
        # 如果旧 MD5 文件不存在，则将旧 MD5 设为空
        old_md5 = ""

    # 如果新 MD5 与旧 MD5 相同，则说明内容没有更新
    if new_md5 == old_md5:
        print("成绩没有更新")
        return
    else:
        # 如果内容有更新，则保存新内容和新的 MD5 值
        save_local(md_content, old_filename)
        with open(md5_filename, 'w', encoding='utf-8') as file:
            file.write(new_md5)
        with open('push_flag.txt', 'w') as file:
            file.write('MD5 changed')

        # 推送成绩更新通知
        score_information_push(md_content, full_name, push_token, success=True)


def save_local(md_content: str, filename: str) -> None:
    # 将内容保存到指定文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(md_content)


def save_md5(md_content: str) -> str:
    # 计算并返回内容的 MD5 哈希值
    return hashlib.md5(md_content.encode('utf-8')).hexdigest()
