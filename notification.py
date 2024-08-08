import requests


def push_notification(token: str, content: str, name: str, success: bool):
    if not token:
        return
    title = f"{name}的自动打卡执行成功" if success else f"**{name}的自动打卡执行失败**"
    data = {
        "title": title,
        "content": content,
        "template": "html"
    }
    try:
        response = requests.post(token, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"通知推送失败: {e}")


def score_information_push(md_content: str, full_name: str, push_token: str):
    if not push_token:
        return
    data = {
        "title": f"{full_name}考试成绩推送",
        "content": md_content,
    }
    try:
        response = requests.post(push_token, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"成绩推送失败: {e}")
