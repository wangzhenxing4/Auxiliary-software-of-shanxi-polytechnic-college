import requests


def push_notification(token: str, content: str, name: str, success: bool):
    """
    发送通知推送

    参数:
    token (str): 推送服务的 API 端点（通常是 URL），用于发送通知
    content (str): 通知内容
    name (str): 用户名，用于构造通知标题
    success (bool): 是否成功标志，用于构造标题

    返回:
    None

    异常:
    requests.RequestException: 如果推送请求失败，打印错误信息
    """
    # 如果 token 为空，则不进行通知推送
    if not token:
        return

    # 根据 success 标志设置通知标题
    title = f"{name}的自动打卡执行成功" if success else f"{name}的自动打卡执行失败"
    data = {
        "title": title,
        "content": content,
        "template": "html"
    }

    try:
        # 发送 POST 请求推送通知
        response = requests.post(token, json=data)
        # 检查请求是否成功
        response.raise_for_status()
    except requests.RequestException as e:
        # 如果推送失败，打印错误信息
        print(f"通知推送失败: {e}")


def score_information_push(md_content: str, full_name: str, push_token: str, success: bool):
    """
    发送成绩信息推送

    参数:
    md_content (str): 成绩信息的内容
    full_name (str): 用户全名，用于构造通知标题
    push_token (str): 推送服务的 API 端点（通常是 URL），用于发送通知
    success (bool): 是否成功标志，用于构造标题

    返回:
    None

    异常:
    requests.RequestException: 如果推送请求失败，打印错误信息
    """
    # 如果 push_token 为空，则不进行成绩信息推送
    if not push_token:
        return

    # 根据 success 标志设置通知标题
    title = f"{full_name}的考试成绩推送执行成功" if success else f"{full_name}的考试成绩推送执行失败"
    data = {
        "title": title,
        "content": md_content,
    }

    try:
        # 发送 POST 请求推送成绩信息
        response = requests.post(push_token, json=data)
        # 检查请求是否成功
        response.raise_for_status()
    except requests.RequestException as e:
        # 如果推送失败，打印错误信息
        print(f"成绩推送失败: {e}")
