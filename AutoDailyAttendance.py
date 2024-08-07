import os
import requests
import urllib.parse
import random
from time import sleep

id_card_number_of_punch_in_person = os.environ.get("ID_NO")
check_in_address_school = os.environ.get("SCHOOL_ADDRESS")
check_in_address_home = os.environ.get("HOLIDAY_ADDRESS")
token = os.environ.get("PUSH_MESSAGE_TOKEN")
CHECK_IN_TIME = '放假'


def retry(func, max_retries=3, delay=1):
    last_exception = None
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            print(f"自动尝试重试，第{attempt + 1}次：{e}")
            sleep(delay)
    raise Exception(f"自动重试达到最大次数：{max_retries}\n错误信息：{last_exception}")


def setup():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; Redmi K30i 5G Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.120 Mobile Safari/537.36 XWEB/1220099 MMWEBSDK/20240404 MMWEBID/5158 MicroMessenger/8.0.49.2600(0x28003154) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Referer": "http://fdcat.cn365vip.com/index103.php?code=0314LBll2jCZHd4cpTol2klxUR14LBlu&state=1"
    }

    # Perform login to get cookies
    login_url = "http://fdcat.cn365vip.com/addu.php"
    response = session.post(login_url, data={"u_name": id_card_number_of_punch_in_person, "upwd": "111111"}, headers=headers)
    response.raise_for_status()
    cookies = session.cookies.get_dict()
    name_of_clock_in_personnel = get_name(cookies)
    return session, headers, name_of_clock_in_personnel


def get_name(cookies):
    if 'unm' in cookies:
        unm = cookies['unm']
        return urllib.parse.unquote(unm)
    else:
        raise Exception("无法获取到打卡人的姓名")


def main():
    session, headers, name_of_clock_in_personnel = setup()
    results = []
    try:
        retry(lambda: login(session, id_card_number_of_punch_in_person, headers))
        temperature, check_in_address = retry(
            lambda: checkin(session, name_of_clock_in_personnel, check_in_address_school, check_in_address_home, headers))
        results.append((name_of_clock_in_personnel, "的自动打卡已成功", f"打卡温度：36.{temperature}，打卡地点：{check_in_address}"))
        push_notification(token, f"**{name_of_clock_in_personnel}的自动打卡执行成功**\n打卡温度：36.{temperature}，打卡地点：{check_in_address}", name_of_clock_in_personnel, success=True)
    except Exception as e:
        results.append((name_of_clock_in_personnel, f"错误原因：{e}"))
        print(f"自动打卡失败：{e}")
        push_notification(token, f"自动打卡失败\n错误原因：{e}", name_of_clock_in_personnel, success=False)
    finally:
        session.close()
    return results


def login(session, id_card_number_of_punch_in_person, headers):
    login_url = "http://fdcat.cn365vip.com/addu.php"
    response = session.post(login_url, data={"u_name": id_card_number_of_punch_in_person, "upwd": "111111"}, headers=headers)
    response.raise_for_status()


def checkin(session, name_of_clock_in_personnel, check_in_address_school, check_in_address_home, headers):
    checkin_url = "http://fdcat.cn365vip.com/adddt_s2_up.php"
    check_in_address = check_in_address_home if CHECK_IN_TIME == '放假' else check_in_address_school
    temperature = str(random.randint(0, 9))
    payload = {
        "u_addr": check_in_address,
        "vname": name_of_clock_in_personnel,
        "tw1": "36",
        "tw2": temperature,
    }
    response = session.post(checkin_url, data=payload, headers=headers)
    response.raise_for_status()
    return temperature, check_in_address


def push_notification(url, content, name_of_clock_in_personnel, success):
    if not url:
        return
    title = f"{name_of_clock_in_personnel}的自动打卡执行成功" if success else f"**{name_of_clock_in_personnel}的自动打卡执行失败**"
    data = {
        "title": title,
        "content": content,
        "template": "html"
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"推送失败：{e}")


if __name__ == "__main__":
    main()
