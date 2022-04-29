from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, HttpResponse
from .forms import *
from django.contrib import messages
from .serializers import EmployeRegisterSerializer, EmployeSerializer, UserRegisterSerialerz
# Create your views here.

def error_500(request, username):
    return render(request, '500.html')


def error_404(request, username):
    return render(request, '404.html')



def user_registor(request, username):
    if request.user.username != username:
        return redirect('error' , username)
    else:
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        postion = Postion.objects.filter(id=employe.position.id)
        users = User.objects.all().count()
        user_count = AdduserCount.objects.first()
        for el in postion:
            if request.user.username !=username or el.position == "worker" or el.position == "deputy":
                return redirect('error' , username)
            elif users < user_count.users:
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
            else:
                return HttpResponse("You do not have permission to add a new user !!!")

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

            try:
                name_error = User.objects.get(username=username)
                messages.error(request,'Password error')
            except:
                messages.error(request, 'Login error')
    
    context = {
        'form':form
    }
    return render(request, 'SignIn.html', context)

def logout_user(request):
    logout(request)
    return redirect('user_login')


def user_profile(request, username):
    user = User.objects.get(username=username)
    admin = User.objects.get(username=request.user.username)
    admin_employe = Employe.objects.get(user=admin)
    employe = Employe.objects.get(user=user)
    position1 = Postion.objects.get(id=admin_employe.position.id)
    section = Section.objects.get(id=admin_employe.section.id)
    user_change = AdminChange(request.POST or None, instance=employe)
    user_count =  AdduserCount.objects.first()
    user_add = AddUser(request.POST or None, request.FILES or None, instance=user_count)
    if request.method == 'POST':
        user_add = AddUser(request.POST, request.FILES, instance=user_count)
        user_change = AdminChange(request.POST, request.FILES, instance=employe)
        if user_change.is_valid() or user_add.is_valid():
            if section.id==employe.section.id or request.user.is_superuser:
                user_change.save()
            if request.user.is_superuser:
                user_add.save()
            return redirect('user_profile', user.username)

    context = {
        'employe':employe,
        'user_change':user_change,
        'position1':position1,
        'section':section,
        'user':user,
        'adduser':user_add,
        'admin':admin,
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
                employe_filt = Employe.objects.get(user=user)
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
                    'users_dict':users_list,
                    'employe_filt':employe_filt
                }
            else:
                employe_filter = Employe.objects.get(user=user)
                users_list = []
                employes_list = []
                employe = Employe.objects.all()
                employe_filt = Employe.objects.get(user=user)
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
                    'users_dict':users_list,
                    'employe_filt':employe_filt
                }
            if request.method == 'POST':
                position = PositionForm(request.POST, request.FILES)
                if position.is_valid():
                    position.save()
                    return redirect('user_registor', username)
    return render(request, 'account/employe.html', context)








def user_tablets(request, username):
    if request.user.username !=username:
        return redirect('error', username)
    else:
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        position1 = Postion.objects.get(id=employe.position.id)
        if request.user.username !=username or position1.position != "director":
            return redirect('error', username)
        elif Employe.objects.filter(user=user):
            user = User.objects.get(username=username)
            employe = Employe.objects.get(user=user)
            position1 = Postion.objects.get(id=employe.position.id)
            section = Section.objects.get(id=employe.section.id)
            employes = Employe.objects.all()
    context = {
        'position1':position1,
        'employes':employes,
        'section':section,
    }
    return render(request, 'basic_tablets.html', context)

def delete_employe(request, username):
    user = User.objects.get(username=username)
    employe = Employe.objects.get(user=user)
    employe.delete()
    return redirect('user_tablets', request.user.username)


class UserRegister(APIView):
    def post(self, request):
        user = UserRegisterSerialerz(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response({'user':user.data})


class RegisterEmploye(APIView):
    def post(self, request, username):
        user = User.objects.get(username=username)
        author = Employe.objects.get(author=user)
        employe = EmployeRegisterSerializer(author, data=request.data)
        employe.is_valid(raise_exception=True)
        employe.save()
        return Response({'employe':employe.data}, status=status.HTTP_200_OK)


class GetEmploye(APIView):
    def get(self, request, username):
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        serializer = EmployeSerializer(employe)
        return Response(serializer.data)