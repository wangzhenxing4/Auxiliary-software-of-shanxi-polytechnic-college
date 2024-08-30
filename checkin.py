import requests
import random
from config import CHECK_IN_TIME, check_in_address_school, check_in_address_home
from ExtractInformation import get_name
from utils import get_user_agent
from retry import retry


def login(session, id_card_number_of_punch_in_person, headers):
    login_url = "http://fdcat.cn365vip.com/addu.php"
    response = session.post(login_url, data={"u_name": id_card_number_of_punch_in_person, "upwd": "111111"}, headers=headers)
    response.raise_for_status()


def checkin(session, name_of_clock_in_personnel, headers):
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


@retry(retries=3, delay=1, backoff=2)
def perform_checkin(id_card_number_of_punch_in_person):
    session, headers, name_of_clock_in_personnel = setup(id_card_number_of_punch_in_person)
    login(session, id_card_number_of_punch_in_person, headers)
    temperature, check_in_address = checkin(session, name_of_clock_in_personnel, headers)
    return name_of_clock_in_personnel, temperature, check_in_address


def setup(id_card_number_of_punch_in_person):
    session = requests.Session()
    headers = {"User-Agent": get_user_agent()}
    login(session, id_card_number_of_punch_in_person, headers)
    cookies = session.cookies.get_dict()
    name_of_clock_in_personnel = get_name(cookies)
    return session, headers, name_of_clock_in_personnel
