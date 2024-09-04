from bs4 import BeautifulSoup
from utils import get_user_agent
from config import student_id, password
from login import login_jwxt

# 请输入你的ID数字
kcid = '0'

def rerun(check_id):
    # 尝试登录教务系统，获取会话和用户全名
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

    # 构造动态表单字段名
    # 将用户输入的id转换为表单字段名，例如将 `kcmcGrid_xk_0` 转换为 `kcmcGrid$ctl02$xk`
    field_name = check_id.replace("_xk_", "$ctl0").replace("kcmcGrid_xk_", "kcmcGrid$ctl") + "$xk"

    # 模拟勾选复选框和提交表单
    data = {
        '__VIEWSTATE': viewstate,
        '__EVENTVALIDATION': eventvalidation,
        'kcmcGrid$ctl02$xk':'on',
        'Button1': '   提 交  ',  # 提交按钮
    }

    # 发送 POST 请求提交表单
    post_response = session.post(url, headers=headers, data=data)
    post_response.raise_for_status()

    # 打印响应结果
    print(post_response.text)

if __name__ == "__main__":
    # 用户输入的复选框 id
    check_id = f"kcmcGrid_xk_{kcid}"
    rerun(check_id)
    # print(check_id)
