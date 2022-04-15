from django.shortcuts import redirect, render
from django.contrib.auth.forms import authenticate
from account.models import User, Employe
from account.models import Postion, AdduserCount
# Create your views here.

def dashboard(request, username):
    if request.user.username !=username:
        return redirect('error', username)
    else:
        user = User.objects.get(username=username)
        if request.user.username !=username:
            return redirect('error', username)
        elif Employe.objects.filter(user=user):
            user = User.objects.get(username=username)
            employe = Employe.objects.get(user=user)
            position1 = Postion.objects.get(id=employe.position.id)
            user_count = User.objects.all().count()
            employes = Employe.objects.all()
            users = User.objects.all()
            for i in AdduserCount.objects.all():
                procent = (user_count*100)/i.users
        else:
            return redirect('erorr_505', username)
    context = {
        'user':user,
        'employe':employe,
        'procent':procent,
        'position1':position1,
        'user_count':user_count,
        'employes':employes,
        'users':users
    }
    return render(request, 'dashboard.html', context)