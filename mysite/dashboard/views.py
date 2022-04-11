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
    context = {
        'user':user,
        'employe':employe,
    }


    return render(request, 'dashboard.html', context)