import sys
from config import student_id, password, token
from ReadSetting import read_setting
from login import login_jwxt
from ObtainGrades import fetch_student_grades
from ExtractGrades import extract_grades
from SaveGrades import save
from notification import score_information_push


def rerun():
    setting_file_path = "Switch"
    score_update_reminder = read_setting(setting_file_path)
    if score_update_reminder == "关闭":
        return

    try:
        session, full_name = login_jwxt(student_id, password)
        cookies = session.cookies.get_dict()
        response = fetch_student_grades(student_id, cookies)
        md_content = extract_grades(response)
        save(md_content, full_name, token)
    except ValueError as e:
        error_message = f"终止程序: {e}" if "密码错误" in str(e) else f"发生错误: {e}"
        print(f"[ERROR] {error_message}")
        try:
            score_information_push(error_message, "你", token, success=False)
        except Exception as push_error:
            print(f"[ERROR] 发送通知失败: {push_error}")
        sys.exit(1)
    except Exception as e:
        error_message = f"发生未预期的错误: {e}"
        print(f"[ERROR] {error_message}")
        try:
            score_information_push(error_message, "你", token, success=False)
        except Exception as push_error:
            print(f"[ERROR] 发送通知失败: {push_error}")
        sys.exit(1)


if __name__ == "__main__":
    rerun()
