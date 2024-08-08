from config import student_id, password, token
from utils import read_setting
from login import login_jwxt, fetch_id_card_number
from checkin import perform_checkin
from notification import push_notification


def main():
    setting_file_path = "Switch"
    auto_daily_attendance = read_setting(setting_file_path)
    if auto_daily_attendance == "关闭":
        return
    session, full_name = login_jwxt(student_id, password)
    id_card_number_of_punch_in_person = fetch_id_card_number(session, student_id)
    results = []
    name_of_clock_in_personnel = None
    try:
        name_of_clock_in_personnel, temperature, check_in_address = perform_checkin(id_card_number_of_punch_in_person)
        results.append(
            (name_of_clock_in_personnel, "的自动打卡已成功", f"打卡温度：36.{temperature}，打卡地点：{check_in_address}"))
        push_notification(token,
                          f"**{name_of_clock_in_personnel}的自动打卡执行成功**\n打卡温度：36.{temperature}，打卡地点：{check_in_address}",
                          name_of_clock_in_personnel, success=True)
    except Exception as e:
        if name_of_clock_in_personnel is None:
            name_of_clock_in_personnel = "未知"
        results.append((name_of_clock_in_personnel, f"错误原因：{e}"))
        push_notification(token, f"自动打卡失败\n错误原因：{e}", name_of_clock_in_personnel, success=False)
    finally:
        session.close()
    return results


if __name__ == "__main__":
    main()
