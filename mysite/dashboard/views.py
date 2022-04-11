from multiprocessing import context
from re import S
from turtle import position
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import authenticate
from account.models import User, Employe
from account.models import Postion
# Create your views here.


def dashboard(request, username):

    if request.user.username !=username:
        return HttpResponse('NO HACKING')
    else:
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        position = Postion.objects.filter(id=employe.position.id)
        user_count = User.objects.all().count()
        s = 22
        procent = (user_count*100)/s
    context = {
        'user':user,
        'employe':employe,
        'procent':procent,
        'position':position
    }


    return render(request, 'dashboard.html', context)