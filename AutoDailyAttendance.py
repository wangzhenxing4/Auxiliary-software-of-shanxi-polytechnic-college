import sys
from config import id_card_number_of_punch_in_person, token
# from config import student_id, password, token
# from login import login_jwxt_ttdk
from notification import push_notification
from ReadSetting import read_setting_AutoDailyAttendance
# from ExtractInformation import fetch_id_card_number
from checkin import perform_checkin


def main():
    """
    主函数，执行自动打卡流程

    - 读取设置文件，检查是否启用自动打卡功能
    - 执行打卡操作
    - 处理打卡结果并推送通知
    """
    setting_file_path = "Switch" # 本功能的开关文件
    auto_daily_attendance = read_setting_AutoDailyAttendance(setting_file_path) # 读取开关内容
    if auto_daily_attendance == "关闭":
        return  # 如果自动打卡功能关闭，则直接返回

    session = None
    try:
        # 登录和获取打卡人的身份证号码的代码被注释掉
        # session = login_jwxt_ttdk(student_id, password)
        # id_card_number_of_punch_in_person = fetch_id_card_number(session, student_id)

        results = []
        name_of_clock_in_personnel = None
        try:
            # 执行打卡操作
            name_of_clock_in_personnel, temperature, check_in_address = perform_checkin(
                id_card_number_of_punch_in_person)
            results.append((
                name_of_clock_in_personnel, "的自动打卡已成功",
                f"打卡温度：36.{temperature}，打卡地点：{check_in_address}"
            ))
            # 发送成功通知
            push_notification(
                token,
                f"**{name_of_clock_in_personnel}的自动打卡执行成功**\n打卡温度：36.{temperature}，打卡地点：{check_in_address}",
                name_of_clock_in_personnel, success=True
            )
        except Exception as e:
            # 处理打卡失败情况
            if name_of_clock_in_personnel is None:
                name_of_clock_in_personnel = "未知"
            results.append((name_of_clock_in_personnel, f"错误原因：{e}"))
            print(e)  # 打印错误信息
            push_notification(
                token,
                f"自动打卡失败\n错误原因：{e}",
                name_of_clock_in_personnel, success=False
            )
            sys.exit(1)  # 错误时退出程序
    except ValueError as e:
        # 处理 ValueError 异常
        if "密码错误" in str(e):
            push_notification(token, "登录失败：密码错误，程序终止！", "你", success=False)
        else:
            push_notification(token, f"自动打卡失败\n错误原因：{e}", "你", success=False)
        sys.exit(1)  # 错误时退出程序
    except Exception as e:
        # 处理 Exception 异常
        push_notification(token, f"自动打卡失败\n错误原因：{e}", "你", success=False)
        sys.exit(1)  # 错误时退出程序
    finally:
        if session is not None:
            session.close()  # 关闭会话，释放资源

    return results


if __name__ == "__main__":
    main()
