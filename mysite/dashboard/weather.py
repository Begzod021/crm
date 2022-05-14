from django.http import JsonResponse
import requests


def get_weather():
    api_id = 'ebed5a0aec8b2636c1ca0b5cd9174e68'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=' + api_id
    city = 'Tashkent'
    res = requests.get(url.format(city)).json()
    temp = res["main"]["temp"]
    temp_c = temp - 273.15
    city_info = {
        'city':city,
        'temp':int(temp_c),
        'icon':res["weather"][0]["icon"],
        'description':res["weather"][0]["description"]
    }
    return city_info