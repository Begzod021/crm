import requests


def get_course():

    response_get = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()

    course_info = {
        "name_dollar":response_get[0]["Ccy"],
        "name_euro":response_get[1]["Ccy"],
        "name_rubl":response_get[2]["Ccy"],
        "course_dollar":response_get[0]["Rate"],
        "course_euro":response_get[1]["Rate"],
        "course_rubl":response_get[2]["Rate"],
        "diff_dollar":response_get[0]["Diff"],
        "diff_euro":response_get[1]["Diff"],
        "diff_rubl":response_get[2]["Diff"]
    }

    return course_info
    