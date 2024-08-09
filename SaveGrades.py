import hashlib
from notification import score_information_push


def save(md_content: str, full_name: str, push_token: str):
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
    else:
        save_local(md_content, old_filename)
        with open(md5_filename, 'w', encoding='utf-8') as file:
            file.write(new_md5)
        with open('push_flag.txt', 'w') as file:
            file.write('MD5 changed')
        score_information_push(md_content, full_name, push_token, success=True)



def save_local(md_content: str, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(md_content)


def save_md5(md_content: str) -> str:
    return hashlib.md5(md_content.encode('utf-8')).hexdigest()
