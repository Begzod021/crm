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
from .weather import weather_get
from .course import get_course
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
        tasks = Task.objects.all()
        task_count = Task.objects.filter(employe=employe).order_by('-id')
        count_todos = task_count.count()
        completed_todo = Task.objects.filter(status=True, employe=employes).order_by('-id')
        employe_country = {}
        for el in Employe.COUNTRY:
            employe_country[el[0]] = Employe.get_country(el[0])
        for i in AdduserCount.objects.all():
            procent = (user_count*100)/i.users 
        coursers = get_course()
        weather_get_task = weather_get(employe)
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
        'count_todos':count_todos,
        'completed_todo':completed_todo,
        'tasks':tasks,
        'coursers':coursers,
        'weather_get_task':weather_get_task
    }
    return render(request, 'dashboard.html', context)


def get_weather_json(request):

    user = User.objects.get(username=request.user.username)
    employe = Employe.objects.get(user=user)
    weather = weather_get(employe)

    print(weather["temp"])



    return JsonResponse({'temp':weather["temp"], 'city':weather["city_name"], 'id':weather["id"], 'description':weather["description"],
    "speed":weather["speed"]})