from multiprocessing import context
from re import S
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import authenticate
from account.models import User, Employe
# Create your views here.


def dashboard(request, username):

    if request.user.username !=username:
        return HttpResponse('NO HACKING')
    try:
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
    except User.DoesNotExist:
        return redirect('user_registor')
    context = {
        'user':user,
        'employe':employe,
    }


    return render(request, 'dashboard.html', context)