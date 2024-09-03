import requests
import random
from config import CHECK_IN_TIME, check_in_address_school, check_in_address_home
from ExtractInformation import get_name
from utils import get_user_agent
from retry import retry


def login(session: requests.Session, id_card_number_of_punch_in_person: str, headers: dict) -> None:
    """
    执行登录操作

    参数:
    session (requests.Session): 已经建立的会话对象
    id_card_number_of_punch_in_person (str): 打卡人的身份证号码
    headers (dict): 请求头信息

    异常:
    requests.RequestException: 如果请求失败
    """
    login_url = "http://fdcat.cn365vip.com/addu.php" # 打卡页面登录页面路径
    response = session.post(login_url, data={"u_name": id_card_number_of_punch_in_person, "upwd": "111111"}, headers=headers) # 提交登录信息
    response.raise_for_status()  # 确保请求成功


def checkin(session: requests.Session, name_of_clock_in_personnel: str, headers: dict) -> tuple[str, str]:
    """
    执行打卡操作

    参数:
    session (requests.Session): 已经建立的会话对象
    name_of_clock_in_personnel (str): 打卡人的姓名
    headers (dict): 请求头信息

    返回:
    tuple: 包含随机生成的温度和打卡地址的元组 (temperature, check_in_address)

    异常:
    requests.RequestException: 如果请求失败
    """
    checkin_url = "http://fdcat.cn365vip.com/adddt_s2_up.php" # 打卡执行操作页面路径
    check_in_address = check_in_address_home if CHECK_IN_TIME == '放假' else check_in_address_school # 判断打卡位置
    temperature = str(random.randint(0, 9))  # 生成随机温度
    payload = {
        "u_addr": check_in_address, # 判断打卡位置
        "vname": name_of_clock_in_personnel, # 打卡人员姓名
        "tw1": "36",  # 固定体温值
        "tw2": temperature,  # 随机生成的体温值
    }
    response = session.post(checkin_url, data=payload, headers=headers)
    response.raise_for_status()  # 确保请求成功
    return temperature, check_in_address


@retry(retries=3, delay=1, backoff=2)
def perform_checkin(id_card_number_of_punch_in_person: str) -> tuple[str, str, str]:
    """
    执行打卡流程，包括登录和打卡

    参数:
    id_card_number_of_punch_in_person (str): 打卡人的身份证号码

    返回:
    tuple: 包含打卡人姓名、随机生成的温度和打卡地址的元组 (name_of_clock_in_personnel, temperature, check_in_address)
    """
    session, headers, name_of_clock_in_personnel = setup(id_card_number_of_punch_in_person)
    login(session, id_card_number_of_punch_in_person, headers)
    temperature, check_in_address = checkin(session, name_of_clock_in_personnel, headers)
    return name_of_clock_in_personnel, temperature, check_in_address


def setup(id_card_number_of_punch_in_person: str) -> tuple[requests.Session, dict, str]:
    """
    设置会话，进行登录并获取打卡人姓名

    参数:
    id_card_number_of_punch_in_person (str): 打卡人的身份证号码

    返回:
    tuple: 包含会话对象、请求头信息和打卡人姓名的元组 (session, headers, name_of_clock_in_personnel)
    """
    session = requests.Session()
    headers = {"User-Agent": get_user_agent()}
    login(session, id_card_number_of_punch_in_person, headers)
    cookies = session.cookies.get_dict()
    name_of_clock_in_personnel = get_name(cookies)
    return session, headers, name_of_clock_in_personnel
