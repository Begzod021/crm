from multiprocessing import context
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import authenticate
from account.models import User, Employe
from account.models import Postion, AdduserCount
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from task.models import Task
from django.conf import settings
import requests
from .models import City
from .forms import CityForm
# Create your views here.


@login_required(login_url='user_login')
def dashboard(request, username):
    if request.user.username !=username:
        return redirect('error', username)
    else:
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        position1 = Postion.objects.get(id=employe.position.id)
        user_count = User.objects.all().count()
        employes = Employe.objects.all()
        users = User.objects.all()
        task_count = Task.objects.filter(employe=employe)
        employe_country = {}
        for el in Employe.COUNTRY:
            employe_country[el[0]] = Employe.get_country(el[0])
        for i in AdduserCount.objects.all():
            procent = (user_count*100)/i.users
    context = {
        'user':user,
        'employe':employe,
        'procent':procent,
        'position1':position1,
        'user_count':user_count,
        'employes':employes,
        'users':users,
        'task_count':task_count,
        'employe_country':list(employe_country.values()),
 
    }
    return render(request, 'dashboard.html', context)








def get_weather_data(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city_name,
        'appid': settings.OWM_API_KEY,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    json_response = response.json()

    weather_data = {
        'temp': json_response['main']['temp'],
        'temp_min': json_response['main']['temp_min'],
        'temp_max': json_response['main']['temp_max'],
        'city_name': json_response['name'],
        'country': json_response['sys']['country'],
        'lat': json_response['coord']['lat'],
        'lon': json_response['coord']['lon'],
        'weather': json_response['weather'][0]['main'],
        'weather_desc': json_response['weather'][0]['description'],
        'pressure': json_response['main']['pressure'],
        'humidity': json_response['main']['humidity'],
        'wind_speed': json_response['wind']['speed'],
    }
    return weather_data


def home(request, username):
    form = CityForm()
    user = User.objects.get(username=username)
    employe = Employe.objects.get(user=user)
    position1 = Postion.objects.get(id=employe.position.id)
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            city_name = form.cleaned_data.get('city_name')
            weather_data = get_weather_data(city_name)
            

    elif request.method == 'GET':
        try:
            city_name = City.objects.latest('date_added').city_name
            weather_data = get_weather_data(city_name)
        except Exception as e:
            weather_data = None
            
    template_name = 'weather.html'
    context = {'form': form, 'weather_data': weather_data,
    'user':user, 'position1':position1, 'employe':employe}
    return render(request, template_name, context=context)