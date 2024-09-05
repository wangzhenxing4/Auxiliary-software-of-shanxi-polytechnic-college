from bs4 import BeautifulSoup
from utils import get_user_agent
from config import student_id, password, course_id, course_id2
from login import login_jwxt


def rerun(check_id):
    session, full_name = login_jwxt(student_id, password)

    # 获取会话的 Cookies
    cookies = session.cookies.get_dict()

    # 请求选课页面 URL
    url = f"http://222.199.6.17/xf_xsqxxxk.aspx?xh={student_id}"

    # 构造 HTTP 请求头
    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "Referer": url,
        "User-Agent": get_user_agent(),
    }

    # 发送 GET 请求以获取页面内容
    response = session.get(url, headers=headers)
    response.raise_for_status()  # 检查请求是否成功
    html_content = response.text

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取隐藏字段 __VIEWSTATE 和 __EVENTVALIDATION
    viewstate = soup.find('input', {'id': '__VIEWSTATE'}).get('value')
    eventvalidation = soup.find('input', {'id': '__EVENTVALIDATION'}).get('value')

    # 查找具有指定 ID 的元素
    element = soup.find(id=check_id)

    # 确保元素存在并获取 name 属性的值
    if element:
        field_name = element.get('name')
    else:
        print(f"Element with ID {check_id} not found.")
        return False

    # 模拟勾选复选框和提交表单
    data = {
        '__VIEWSTATE': viewstate,
        '__EVENTVALIDATION': eventvalidation,
        field_name: 'on',
        'Button1': '   提 交  ',  # 提交按钮
    }

    # 发送 POST 请求提交表单
    post_response = session.post(url, headers=headers, data=data)
    post_response.raise_for_status()

    # 打印响应结果
    response_text = post_response.text
    print(response_text)

    # 检查是否提示人数超过限制
    if ("人数超过限制！！" in response_text or
            "上课时间冲突！！" in response_text):
        return False
    return True


if __name__ == "__main__":
    # 先尝试kcid1和kcid2
    initial_ids = [course_id, course_id2]
    for cid in initial_ids:
        check_id = f"kcmcGrid_xk_{cid - 1}"
        if rerun(check_id):
            print(f"Success with check_id: {check_id}")
            break
    else:
        # 如果kcid1和kcid2都失败，尝试1到10的ID
        for cid in range(1, 15):
            check_id = f"kcmcGrid_xk_{cid - 1}"
            if rerun(check_id):
                print(f"Success with check_id: {check_id}")
                break
        else:
            print("All attempts failed.")
