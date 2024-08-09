from config import student_id, password, token
from ReadSetting import read_setting
from login import login_jwxt
from ObtainGrades import fetch_student_grades
from ExtractGrades import extract_grades
from SaveGrades import save


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
