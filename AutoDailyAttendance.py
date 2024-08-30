import sys
from config import id_card_number_of_punch_in_person, token
# from config import student_id, password , token
# from login import login_jwxt_ttdk
from notification import push_notification
from ReadSetting import read_setting_auto_daily_attendance
# from ExtractInformation import fetch_id_card_number
from checkin import perform_checkin


def main():
    # 设定配置文件路径
    setting_file_path = "Switch"

    # 读取自动打卡设置
    auto_daily_attendance = read_setting_auto_daily_attendance(setting_file_path)

    # 如果自动打卡设置为"关闭"，则结束程序
    if auto_daily_attendance == "关闭":
        return

    session = None
    try:
        # 如果有需要，登录系统的代码可以在这里执行
        # session = login_jwxt_ttdk(student_id, password)
        # id_card_number_of_punch_in_person = fetch_id_card_number(session, student_id)

        results = []
        name_of_clock_in_personnel = None

        try:
            # 执行打卡操作
            name_of_clock_in_personnel, temperature, check_in_address = perform_checkin(
                id_card_number_of_punch_in_person)

            # 打卡成功，记录结果并发送成功通知
            results.append(
                (name_of_clock_in_personnel, "的自动打卡已成功",
                 f"打卡温度：36.{temperature}，打卡地点：{check_in_address}"))
            push_notification(token,
                              f"**{name_of_clock_in_personnel}的自动打卡执行成功**\n打卡温度：36.{temperature}，打卡地点：{check_in_address}",
                              name_of_clock_in_personnel, success=True)
        except Exception as e:
            # 捕获打卡过程中出现的异常
            if name_of_clock_in_personnel is None:
                name_of_clock_in_personnel = "未知"
            results.append((name_of_clock_in_personnel, f"错误原因：{e}"))
            print(e)
            # 发送失败通知
            push_notification(token, f"自动打卡失败\n错误原因：{e}", name_of_clock_in_personnel, success=False)
            sys.exit(1)  # 退出程序，并返回错误状态码

    except ValueError as e:
        # 处理特定的值错误，例如密码错误
        if "密码错误" in str(e):
            push_notification(token, "登录失败：密码错误，程序终止！", "你", success=False)
        else:
            push_notification(token, f"自动打卡失败\n错误原因：{e}", "你", success=False)
        sys.exit(1)  # 退出程序，并返回错误状态码

    except Exception as e:
        # 处理其他异常
        push_notification(token, f"自动打卡失败\n错误原因：{e}", "你", success=False)
        sys.exit(1)  # 退出程序，并返回错误状态码

    finally:
        # 清理资源，关闭 session（如果存在）
        if session is not None:
            session.close()

    return results


if __name__ == "__main__":
    # 执行主函数
    main()
