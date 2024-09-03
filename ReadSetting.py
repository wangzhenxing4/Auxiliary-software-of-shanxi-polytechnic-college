def read_setting(file_path):
    """
    从指定配置文件中读取设置项

    参数:
    file_path (str): 配置文件路径

    返回:
    str: "ScoreUpdateReminder" 设置项的值，如果配置文件中未找到该设置项，则返回 "关闭"

    异常:
    FileNotFoundError: 如果指定的配置文件未找到
    Exception: 如果读取配置文件时发生其他错误
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("ScoreUpdateReminder"):
                    # 返回 "ScoreUpdateReminder" 设置项的值
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        # 如果文件未找到，则抛出异常
        raise Exception(f"未找到配置文件: {file_path}")
    except Exception as e:
        # 处理其他异常
        raise Exception(f"读取配置文件时出错: {e}")
    # 如果配置文件中没有找到设置项，则返回默认值 "关闭"
    return "关闭"


def read_setting_AutoDailyAttendance(file_path):
    """
    从指定配置文件中读取设置项

    参数:
    file_path (str): 配置文件路径

    返回:
    str: "AutoDailyAttendance" 设置项的值，如果配置文件中未找到该设置项，则返回 "关闭"

    异常:
    FileNotFoundError: 如果指定的配置文件未找到
    Exception: 如果读取配置文件时发生其他错误
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("AutoDailyAttendance"):
                    # 返回 "AutoDailyAttendance" 设置项的值
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        # 如果文件未找到，则抛出异常
        raise Exception(f"未找到配置文件: {file_path}")
    except Exception as e:
        # 处理其他异常
        raise Exception(f"读取配置文件时出错: {e}")
    # 如果配置文件中没有找到设置项，则返回默认值 "关闭"
    return "关闭"
