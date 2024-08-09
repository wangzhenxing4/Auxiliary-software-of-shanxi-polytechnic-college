import requests
import re
from utils import get_user_agent
from decrypt import extract_from_html


def fetch_student_grades(student_id: str, cookies: dict) -> requests.Response:
    url = f"http://jwgl.sxzy.edu.cn/xscjcx.aspx?xh={student_id}"
    headers = {
        "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "Referer": url,
        "User-Agent": get_user_agent()
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text
    viewstate = extract_from_html(r'id="__VIEWSTATE" value="([^"]+)"', html_content)
    eventvalidation = extract_from_html(r'id="__EVENTVALIDATION" value="([^"]+)"', html_content)
    if not viewstate or not eventvalidation:
        raise ValueError("无法获取成绩")
    data = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": eventvalidation,
        "ddlXN": "2023-2024",
        "ddlXQ": "2",
        "btn_xq": "学期成绩"
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response


def extract_grades(response: requests.Response) -> str:
    html_content = response.text
    pattern = re.compile(
        r'<tr(?: class="alt")?>\s*<td>(?P<year>\d{4}-\d{4})</td>\s*<td>(?P<term>\d)</td>\s*<td>(?P<course_code>\d+)</td>\s*<td>(?P<course_name>.*?)</td>\s*<td>(?P<course_nature>.*?)</td>\s*<td>(?P<course_affiliation>&nbsp;|.*?)</td>\s*<td>(?P<credit>[\d.]+)</td>\s*<td>(?P<grade_point>[\d.]+)</td>\s*<td>(?P<score>[\d.]+|优秀|良好|及格|不及格)</td>\s*<td>(?P<minor_flag>\d+)</td>\s*<td>(?P<makeup_score>&nbsp;|.*?)</td>\s*<td>(?P<retake_score>&nbsp;|.*?)</td>\s*<td>(?P<teaching_department>.*?)</td>\s*<td>(?P<remark>.*?)</td>\s*<td>(?P<retake_flag>.*?)</td>\s*</tr>'
    )
    matches = pattern.findall(html_content)
    score_summary = []
    for match in matches:
        course_info = {
            "学年": match[0],
            "学期": match[1],
            "课程代号": match[2],
            "课程名称": match[3],
            "课程性质": match[4],
            "学分": match[6],
            "绩点": match[7],
            "成绩": match[8],
            "开设学院": match[12]
        }
        score_summary.append(course_info)

    md_content = "\n\n".join(
        f"### 课程名称: {course['课程名称']}\n"
        f"- **课程性质**: {course['课程性质']}\n"
        f"- **学年**: {course['学年']}\n"
        f"- **学期**: {course['学期']}\n"
        f"- **课程代码**: {course['课程代号']}\n"
        f"- **学分**: {course['学分']}\n"
        f"- **绩点**: {course['绩点']}\n"
        f"- **成绩**: {course['成绩']}\n"
        f"- **开设学院**: {course['开设学院']}"
        for course in score_summary
    )
    return md_content
