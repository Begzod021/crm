from multiprocessing import context
from django.conf import UserSettingsHolder
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render, HttpResponse
from .forms import *
# Create your views here.

def error_404(request, username):
    user = User.objects.get(username=username)
    employe = Employe.objects.filter(user=user)

    context = {
        'employe':employe
    }
    return render(request, '404.html', context)



def user_registor(request, username):
    user = User.objects.get(username=username)
    employe = Employe.objects.get(user=user)
    postion = Postion.objects.filter(id=employe.position.id)
    for el in postion:
        if request.user.username !=username or el.position == "worker" or el.position == "deputy":
            return redirect('error' , username)
        else:
            form = AddAdmin()
            if request.method == 'POST':
                form = AddAdmin(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.save()
                    return redirect('employe', username)
                else:
                    return redirect('user_registor', username)

    context = {
        'form':form,
    }


    return render(request, 'SignUp.html', context)


def user_login(request):
    form = AddAdmin()
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard', user.username)
        else:
            return redirect('user_registor')
    
    context = {
        'form':form
    }
    return render(request, 'SignIn.html', context)

def logout_user(request):
    logout(request)
    return redirect('user_login')


def user_profile(request, slug):
    employe = Employe.objects.get(slug=slug)
    user_change = AdminChange(instance=employe)
    if request.method == 'POST':
        user_change = AdminChange(request.POST, request.FILES, instance=employe)
        print('1')
        if user_change.is_valid():
            print('2')
            user_change.save()
            return redirect('user_profile', employe.slug)
    
    context = {
        'employe':employe,
        'user_change':user_change,
    }

    return render(request, 'account/profile.html', context)

def employe(request, username):
    user = User.objects.get(username=username)
    employes = Employe.objects.get(user=user)
    postion = Postion.objects.filter(id=employes.position.id)
    for el in postion:
        if request.user.username !=username or el.position == "worker" or el.position == "deputy":
             return redirect('error', username)
        else:
            user = User.objects.get(username=username)
            employe = Employe.objects.filter(user=user)
            position = PositionForm()
            if request.method == 'POST':
                position = PositionForm(request.POST, request.FILES)
                if position.is_valid():
                    position.save()
                    return redirect('employe', username)
                else:
                    return HttpResponse('REGISTER HAS DONE')
    context = {
        'position':position,
        'employe':employe,
    }
    return render(request, 'account/employe.html', context)