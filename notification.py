import requests


def push_notification(token: str, content: str, name: str, success: bool):
    """
    发送通知推送，告知自动打卡操作的结果。

    参数:
    - token: 用于发送通知的推送服务 API 地址。
    - content: 通知内容。
    - name: 打卡人的姓名。
    - success: 标记操作是否成功，成功为 True，失败为 False。

    返回值:
    - 无返回值。
    """
    if not token:
        # 如果没有提供 token，则不进行推送
        return

    # 根据操作是否成功设置通知标题
    title = f"{name}的自动打卡执行成功" if success else f"{name}的自动打卡执行失败"

    # 构建发送的数据
    data = {
        "title": title,
        "content": content,
        "template": "html"
    }

    try:
        # 发送 POST 请求以推送通知
        response = requests.post(token, json=data)
        # 确保请求成功
        response.raise_for_status()
    except requests.RequestException as e:
        # 如果请求失败，打印错误信息
        print(f"通知推送失败: {e}")


def score_information_push(md_content: str, full_name: str, push_token: str, success: bool):
    """
    推送考试成绩信息，告知成绩推送操作的结果。

    参数:
    - md_content: Markdown 格式的成绩信息内容。
    - full_name: 学生的全名。
    - push_token: 用于发送推送的服务 API 地址。
    - success: 标记操作是否成功，成功为 True，失败为 False。

    返回值:
    - 无返回值。
    """
    if not push_token:
        # 如果没有提供推送 token，则不进行推送
        return

    # 根据操作是否成功设置通知标题
    title = f"{full_name}的考试成绩推送执行成功" if success else f"{full_name}的考试成绩推送执行失败"

    # 构建发送的数据
    data = {
        "title": title,
        "content": md_content,
    }

    try:
        # 发送 POST 请求以推送成绩信息
        response = requests.post(push_token, json=data)
        # 确保请求成功
        response.raise_for_status()
    except requests.RequestException as e:
        # 如果请求失败，打印错误信息
        print(f"成绩推送失败: {e}")
