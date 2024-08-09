def read_setting(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("ScoreUpdateReminder"):
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        raise Exception(f"未找到配置文件: {file_path}")
    except Exception as e:
        raise Exception(f"读取配置文件时出错: {e}")
    return "关闭"


def read_setting_autodailyattendance(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("AutoDailyAttendance"):
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        raise Exception(f"未找到配置文件: {file_path}")
    except Exception as e:
        raise Exception(f"读取配置文件时出错: {e}")
    return "关闭"
