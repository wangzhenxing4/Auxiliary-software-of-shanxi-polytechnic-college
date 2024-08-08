from config import student_id, password, token
from utils import read_setting, save_local, save_md5
from login import login_jwxt
from grade import fetch_student_grades, extract_grades
from notification import score_information_push


def save(md_content: str, full_name: str, push_token: str):
    if not md_content.strip():
        raise ValueError("内容获取失败")

    old_filename = "成绩.md"
    md5_filename = 'md_content.txt'
    new_md5 = save_md5(md_content)

    try:
        with open(md5_filename, 'r', encoding='utf-8') as file:
            old_md5 = file.read().strip()
    except FileNotFoundError:
        old_md5 = ""

    if new_md5 == old_md5:
        print("成绩没有更新")
    else:
        score_information_push(md_content, full_name, push_token)
        save_local(md_content, old_filename)
        with open(md5_filename, 'w', encoding='utf-8') as file:
            file.write(new_md5)
        with open('push_flag.txt', 'w') as file:
            file.write('MD5 changed')


def rerun(max_retries=3):
    setting_file_path = "Switch"
    score_update_reminder = read_setting(setting_file_path)
    if score_update_reminder == "关闭":
        return
    personnel_data = [(student_id, password, token)]
    for sid, pwd, push_token in personnel_data:
        attempt = 0
        while attempt < max_retries:
            try:
                session, full_name = login_jwxt(sid, pwd)
                cookies = session.cookies.get_dict()
                response = fetch_student_grades(sid, cookies)
                md_content = extract_grades(response)
                save(md_content, full_name, push_token)
                break
            except ValueError as e:
                print(f"尝试失败: {e}")
                attempt += 1
                if attempt >= max_retries:
                    print("已达到最大重试次数")


if __name__ == "__main__":
    rerun()
