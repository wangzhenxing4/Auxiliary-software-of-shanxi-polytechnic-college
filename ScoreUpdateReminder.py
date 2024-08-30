import sys
from config import student_id, password, token
from ReadSetting import read_setting
from login import login_jwxt
from ObtainGrades import fetch_student_grades
from ExtractGrades import extract_grades
from SaveGrades import save
from notification import score_information_push


def rerun():
    """
    主运行函数，检查配置文件中的设置，登录系统，获取并处理成绩信息。
    如果发生错误，会记录错误并发送通知（如有必要），然后退出程序。
    """
    setting_file_path = "Switch"

    # 读取配置文件中的设置
    score_update_reminder = read_setting(setting_file_path)
    if score_update_reminder == "关闭":
        print("成绩更新提醒已关闭，程序终止。")
        return

    try:
        # 登录系统并获取学生姓名
        session, full_name = login_jwxt(student_id, password)

        # 使用 cookies 获取学生成绩
        cookies = session.cookies.get_dict()
        response = fetch_student_grades(student_id, cookies)

        # 解析成绩内容
        md_content = extract_grades(response)

        # 保存成绩内容并发送推送通知
        save(md_content, full_name, token)

    except ValueError as e:
        # 处理 ValueError 异常
        error_message = f"终止程序: {e}" if "密码错误" in str(e) else f"发生错误: {e}"
        print(f"[ERROR] {error_message}")
        if "密码错误" in str(e):
            try:
                score_information_push(error_message, "你", token, success=False)
            except Exception as push_error:
                print(f"[ERROR] 发送通知失败: {push_error}")
        sys.exit(1)
    except Exception as e:
        # 处理其他异常
        print(f"[ERROR] 发生错误: {e}")
        try:
            score_information_push(f"发生错误: {e}", "你", token, success=False)
        except Exception as push_error:
            print(f"[ERROR] 发送通知失败: {push_error}")
        sys.exit(1)


if __name__ == "__main__":
    rerun()
