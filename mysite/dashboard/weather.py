import requests
from django.utils import timezone
from datetime import datetime
import time




def weather_get(employe):
    api_id = 'ebed5a0aec8b2636c1ca0b5cd9174e68'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=' + api_id
    city = employe.country
    res = requests.get(url.format(city)).json()
    temp = res["main"]["temp"]
    temp_c = temp - 273.15
    pressure_kpa = res["main"]["pressure"]
    pressure_b = pressure_kpa / 1000
    date = datetime.today().strftime('%d.%m.%Y')
    city_name = res["name"]

    city_info = {
        'city':city,
        'temp':int(temp_c),
        'icon':res["weather"][0]["icon"],
        'description':res["weather"][0]["description"],
        'id':res["weather"][0]["id"],
        'speed':res["wind"]["speed"],
        'pressure_b':int(pressure_b),
        'city_name':city_name,
        'date':date
    }
    return city_info