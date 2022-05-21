from multiprocessing import context
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, HttpResponse
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from task.models import *
from .models import User, Employe
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from .forms import MyPasswordChangeForm, PasswordResetForm
# Create your views here.
@login_required(login_url='user_login')
def error_500(request, username):
    return render(request, '500.html')

@login_required(login_url='user_login')
def error_404(request, username):
    return render(request, '404.html')


@login_required(login_url='user_login')
def user_registor(request, username):
    if request.user.username != username:
        return redirect('error' , username)
    else:
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        postion = Postion.objects.get(id=employe.position.id)
        users = User.objects.all().count()
        users_token = User.objects.all()
        user_count = AdduserCount.objects.first()
        if postion.position in ('director',) and users < user_count.users:
            form = AddAdmin()
            if request.method == 'POST':
                form = AddAdmin(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.save()
                    for user1 in users_token:
                        Token.objects.get_or_create(user=user1)
                    return redirect('employe', username)
                else:
                    return redirect('user_registor', username)
        else:
            return HttpResponse("You do not have permission to add a new user !!!")
    context = {
        'form':form,
    }


    return render(request, 'SignUp.html', context)


@unauthenticated_user
def user_login(request):
    form = AddAdmin()
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', None)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
                request.session.modified = True
                user1 = User.objects.filter(username=username).update(remember_me=False)
            else:
                user1 = User.objects.filter(username=username).update(remember_me=True)
            return redirect('dashboard', user.username)
        else:
            form = AddAdmin(request.POST, request.FILES)

            try:
                name_error = User.objects.get(username=username)
                messages.error(request, 'Password error')
            except:
                messages.error(request, 'Login error')
    context = {
            'form':form,
        }
    return render(request, 'SignIn.html', context)


def change_password(request, username):
    if request.method == 'POST':
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfuly updated')
            return redirect('user_profile', request.user.username)
        else:
            messages.error(request, 'Please correct the error below.')
        
    else:
        form = MyPasswordChangeForm(request.user)

    return render(request, 'account/change_password.html', {'form':form})









@login_required(login_url='user_login')
def logout_user(request):
    user = User.objects.filter(username=request.user.username).update(remember_me=False, username=request.user.username)
    logout(request)
    return redirect('user_login')



@login_required(login_url='user_login')
def employe(request, username):
    if request.user.username != username:
        return redirect('error', username)
    else:
        user = User.objects.get(username=username)
        employes = Employe.objects.get(user=user)
        postion = Postion.objects.get(id=employes.position.id)
        if postion.position in ('director',):
            user = User.objects.get(username=username)
            position = PositionForm()
            employes = Employe.objects.get(user=user)
            section = Section.objects.get(id=employes.section.id)
            if section.name == "CEO":
                employe = Employe.objects.all()
                users = User.objects.filter(has_profile=False)
                employe_filter = Employe.objects.get(user=user)
                context = {
                    'employe':employe,
                    'position':position,
                    'employe_filter':employe_filter,
                    'users':users
                }
            else:
                employe_filt = Employe.objects.get(user=user)
                employe_filter = Employe.objects.get(user=user)
                employe = Employe.objects.all()
                users = User.objects.filter(has_profile=False)
                context = {
                    'employe_filter':employe_filter,
                    'position':position,
                    'users':users,
                    'employe_filt':employe_filt
                }
            if request.method == 'POST':
                position = PositionForm(request.POST, request.FILES)
                if position.is_valid():
                    position.save()
                    user_id = request.POST.get('user')
                    user_data = User.objects.get(id=user_id)
                    user_data.has_profile_true()
                    user_data.save()
                    employe_email = Employe.objects.filter(user=user_data).update(email=user_data.username + '@crm.com')
                    
                    return redirect('user_registor', username)
        else:
            return redirect('error', username)
    return render(request, 'account/employe.html', context)


@login_required(login_url='user_login')
def user_tablets(request, username):

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
        task_count = Task.objects.filter(employe=employe)
    context = {
        'position1':position1,
        'employes':employes,
        'section':section,
        'task_count':task_count,
        'user':user,
    }
    return render(request, 'basic_tablets.html', context)

def delete_employe(request, username):
    user = User.objects.get(username=username)
    employe = Employe.objects.get(user=user)
    if request.user.username == user.username:
        employe.delete()
        user.delete()
        return redirect('user_login')
    else:
        employe.delete()
        user.delete()
        return redirect('user_tablets', request.user.username)





from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):

    user.profile.is_online = True
    user.profile.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.profile.is_online = False
    user.profile.save()


@login_required(login_url='user_login')
def user_profile(request, username):
    if request.user.username != username:
        return redirect('error', username)
    else:
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        form = AdminChange(request.POST or None, instance=employe)
        position1 = Postion.objects.get(id=employe.position.id)
        section = Section.objects.get(id=employe.section.id)
        user_count =  AdduserCount.objects.first()
        user_add = AddUser(request.POST or None, request.FILES or None, instance=user_count)
        task_count = Task.objects.filter(employe=employe)
        if request.method == 'POST':
            form = AdminChange(request.POST , instance=employe)
            user_add = AddUser(request.POST, request.FILES, instance=user_count)
            if form.is_valid() or user_add.is_valid():
                form.save()
                if request.user.is_superuser:
                    user_add.save()
                return redirect('user_profile', username)

    context = {
        'user':user,
        'employe':employe,
        'form':form,
        'position1':position1,
        'section':section,
        'user_add':user_add,
        'task_count':task_count
    }
    return render(request, 'account/user_profile.html', context)



@login_required(login_url='user_login')
def edit_profile(request, username):
    user = User.objects.get(username=username)
    admin = User.objects.get(username=request.user.username)
    admin_employe = Employe.objects.get(user=admin)
    employe = Employe.objects.get(user=user)
    position1 = Postion.objects.get(id=admin_employe.position.id)
    section = Section.objects.get(id=admin_employe.section.id)
    form = AdminChange(request.POST or None, instance=employe)
    task_count = Task.objects.filter(employe=admin_employe)
    if request.method == 'POST':
        form = AdminChange(request.POST, request.FILES, instance=employe)
        if form.is_valid():
            if section.id==employe.section.id or request.user.is_superuser:
                form.save()
            return redirect('edit_profile', user.username)
    context = {
        'employe':employe,
        'form':form,
        'position1':position1,
        'section':section,
        'user':user,
        'admin':admin,
        'task_count':task_count,
    }
    return render(request, 'account/edit-profile.html', context)


