def read_setting(file_path: str, setting_key: str) -> str:
    """
    从配置文件中读取指定的设置值。

    参数:
    - file_path: 配置文件的路径。
    - setting_key: 要查找的设置键名（例如 "ScoreUpdateReminder"）。

    返回值:
    - 返回设置值，如果配置项未找到则返回 "关闭"。

    异常:
    - 如果配置文件未找到，抛出 FileNotFoundError。
    - 如果读取配置文件时出错，抛出 Exception。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith(setting_key):
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        raise Exception(f"未找到配置文件: {file_path}")
    except Exception as e:
        raise Exception(f"读取配置文件时出错: {e}")
    return "关闭"


def read_setting_score_update_reminder(file_path: str) -> str:
    """
    从配置文件中读取 "ScoreUpdateReminder" 设置值。

    参数:
    - file_path: 配置文件的路径。

    返回值:
    - 返回 "ScoreUpdateReminder" 设置值，如果未找到则返回 "关闭"。
    """
    return read_setting(file_path, "ScoreUpdateReminder")


def read_setting_auto_daily_attendance(file_path: str) -> str:
    """
    从配置文件中读取 "AutoDailyAttendance" 设置值。

    参数:
    - file_path: 配置文件的路径。

    返回值:
    - 返回 "AutoDailyAttendance" 设置值，如果未找到则返回 "关闭"。
    """
    return read_setting(file_path, "AutoDailyAttendance")
