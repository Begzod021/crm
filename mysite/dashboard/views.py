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
        user_count = User.objects.all().count()
        s = 10
        procent = (user_count*100)/s
        print(procent)
        print(user_count)
    context = {
        'user':user,
        'employe':employe,
        'procent':procent
    }


    return render(request, 'dashboard.html', context)