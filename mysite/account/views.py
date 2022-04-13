from multiprocessing import context
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, HttpResponse
from .forms import *
from django.conf import settings
from django.contrib import messages
# Create your views here.

def error_500(request, username):
    user = User.objects.get(username=username)
    context = {
        'user':user

    }
    return render(request, '500.html', context)


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
            form = AddAdmin(request.POST, request.FILES)
            if form.is_valid():
                form = form.cleaned_data['password']
                print(form)
            if password!=form:
                form = AddAdmin()
                messages.error(request, 'password')
            else:
                form = AddAdmin()
                messages.error(request, 'username')
    
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
            position = PositionForm()
            employes = Employe.objects.get(user=user)
            section = Section.objects.get(id=employes.section.id)
            if section.name == "CEO":
                employe = Employe.objects.all()
                users = User.objects.all()
                users_list = []
                employes_list = []
                for i in employe:
                    employes_list.append(i.user)
                    continue
                for j in users:
                    users_list.append(j)
                    continue
                for use in employes_list:
                    for emp in users_list:
                        if use==emp:
                            users_list.remove(emp)
                context = {
                    'employe':employe,
                    'position':position,
                    'users_dict':users_list
                }
            else:
                employe_filter = Employe.objects.get(user=user)
                users_list = []
                employes_list = []
                employe = Employe.objects.all()
                users = User.objects.all()
                for i in employe:
                    employes_list.append(i.user)
                    continue
                for j in users:
                    users_list.append(j)
                    continue
                for use in employes_list:
                    for emp in users_list:
                        if use==emp:
                            users_list.remove(emp)
                context = {
                    'employe_filter':employe_filter,
                    'position':position,
                    'users_dict':users_list
                }
            if request.method == 'POST':
                position = PositionForm(request.POST, request.FILES)
                if position.is_valid():
                    position.save()
                    return redirect('employe', username)
                else:
                    return HttpResponse('REGISTER HAS DONE')
    return render(request, 'account/employe.html', context)