import sys
from config import student_id, password, token
from ReadSetting import read_setting
from login import login_jwxt
from ObtainGrades import fetch_student_grades
from ExtractGrades import extract_grades
from SaveGrades import save
from notification import score_information_push


def rerun():
    # 读取配置文件 "Switch"，获取成绩更新提醒设置
    setting_file_path = "Switch"
    score_update_reminder = read_setting(setting_file_path)

    # 如果成绩更新提醒设置为 "关闭"，则不进行进一步操作
    if score_update_reminder == "关闭":
        return

    try:
        # 尝试登录教务系统，获取会话和用户全名
        session, full_name = login_jwxt(student_id, password)
        # 获取会话的 Cookies
        cookies = session.cookies.get_dict()

        # 获取学生成绩
        response = fetch_student_grades(student_id, cookies)

        # 提取成绩信息
        md_content = extract_grades(response)

        # 保存成绩信息到指定位置
        save(md_content, full_name, token)
    except ValueError as e:
        # 如果发生 ValueError 异常，检查异常信息是否包含 "密码错误"
        error_message = f"终止程序: {e}" if "密码错误" in str(e) else f"发生错误: {e}"
        print(f"[ERROR] {error_message}")

        # 如果错误信息中包含 "密码错误"，则尝试发送通知
        if "密码错误" in str(e):
            try:
                score_information_push(error_message, "你", token, success=False)
            except Exception as push_error:
                # 如果发送通知失败，则输出错误信息
                print(f"[ERROR] 发送通知失败: {push_error}")

        # 终止程序执行
        sys.exit(1)


if __name__ == "__main__":
    # 如果脚本是作为主程序运行，则调用 rerun 函数
    rerun()
