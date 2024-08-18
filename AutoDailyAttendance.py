import sys
from config import id_card_number_of_punch_in_person, token
# from config import student_id, password , token
# from login import login_jwxt_ttdk
from notification import push_notification
from ReadSetting import read_setting_AutoDailyAttendance
# from ExtractInformation import fetch_id_card_number
from checkin import perform_checkin


def main():
    setting_file_path = "Switch"
    auto_daily_attendance = read_setting_AutoDailyAttendance(setting_file_path)
    if auto_daily_attendance == "关闭":
        return
    session = None
    try:
        # session = login_jwxt_ttdk(student_id, password)
        # id_card_number_of_punch_in_person = fetch_id_card_number(session, student_id)
        results = []
        name_of_clock_in_personnel = None
        try:
            name_of_clock_in_personnel, temperature, check_in_address = perform_checkin(
                id_card_number_of_punch_in_person)
            results.append(
                (name_of_clock_in_personnel, "的自动打卡已成功",
                 f"打卡温度：36.{temperature}，打卡地点：{check_in_address}"))
            push_notification(token,
                              f"**{name_of_clock_in_personnel}的自动打卡执行成功**\n打卡温度：36.{temperature}，打卡地点：{check_in_address}",
                              name_of_clock_in_personnel, success=True)
        except Exception as e:
            if name_of_clock_in_personnel is None:
                name_of_clock_in_personnel = "未知"
            results.append((name_of_clock_in_personnel, f"错误原因：{e}"))
            print(e)
            push_notification(token, f"自动打卡失败\n错误原因：{e}", name_of_clock_in_personnel, success=False)
            sys.exit(1)
    except ValueError as e:
        if "密码错误" in str(e):
            push_notification(token, "登录失败：密码错误，程序终止！", "你", success=False)
        else:
            push_notification(token, f"自动打卡失败\n错误原因：{e}", "你", success=False)
        sys.exit(1)
    except Exception as e:
        push_notification(token, f"自动打卡失败\n错误原因：{e}", "你", success=False)
        sys.exit(1)
    finally:
        if session is not None:
            session.close()
    return results


if __name__ == "__main__":
    main()
