import requests
import random
from config import CHECK_IN_TIME, check_in_address_school, check_in_address_home
from ExtractInformation import get_name
from utils import get_user_agent
from retry import retry


def login(session, id_card_number_of_punch_in_person, headers):
    """
    执行登录操作。

    参数:
    - session: requests.Session() 对象，用于发起请求。
    - id_card_number_of_punch_in_person: 打卡人员的身份证号码。
    - headers: 包含请求头的字典，例如 User-Agent。

    返回值:
    - 无返回值。登录操作通过 POST 请求发送数据。
    """
    login_url = "http://fdcat.cn365vip.com/addu.php"
    # 发送 POST 请求进行登录
    response = session.post(
        login_url,
        data={"u_name": id_card_number_of_punch_in_person, "upwd": "111111"},
        headers=headers
    )
    # 确保请求成功，若失败则引发异常
    response.raise_for_status()


def checkin(session, name_of_clock_in_personnel, headers):
    """
    执行打卡操作。

    参数:
    - session: requests.Session() 对象，用于发起请求。
    - name_of_clock_in_personnel: 打卡人员的姓名。
    - headers: 包含请求头的字典，例如 User-Agent。

    返回值:
    - temperature: 打卡时的体温（模拟的随机值）。
    - check_in_address: 打卡地点。
    """
    checkin_url = "http://fdcat.cn365vip.com/adddt_s2_up.php"

    # 根据时间选择打卡地址
    check_in_address = check_in_address_home if CHECK_IN_TIME == '放假' else check_in_address_school

    # 模拟体温值（随机生成0到9之间的整数）
    temperature = str(random.randint(0, 9))

    # 构造打卡请求的负载数据
    payload = {
        "u_addr": check_in_address,
        "vname": name_of_clock_in_personnel,
        "tw1": "36",  # 模拟的体温值，通常为36.0
        "tw2": temperature,  # 体温的后一部分
    }

    # 发送 POST 请求进行打卡
    response = session.post(checkin_url, data=payload, headers=headers)
    # 确保请求成功，若失败则引发异常
    response.raise_for_status()

    return temperature, check_in_address


@retry(retries=3, delay=1, backoff=2)
def perform_checkin(id_card_number_of_punch_in_person):
    """
    执行整个打卡流程，包括登录、获取用户信息和打卡。

    参数:
    - id_card_number_of_punch_in_person: 打卡人员的身份证号码。

    返回值:
    - name_of_clock_in_personnel: 打卡人员的姓名。
    - temperature: 打卡时的体温。
    - check_in_address: 打卡地点。
    """
    session = requests.Session()  # 初始化一个新的会话
    headers = {"User-Agent": get_user_agent()}  # 获取用户代理

    # 执行登录操作
    login(session, id_card_number_of_punch_in_person, headers)

    # 从 session 中获取 cookies 并通过 cookies 获取用户姓名
    cookies = session.cookies.get_dict()
    name_of_clock_in_personnel = get_name(cookies)

    # 执行打卡操作
    temperature, check_in_address = checkin(session, name_of_clock_in_personnel, headers)

    return name_of_clock_in_personnel, temperature, check_in_address
