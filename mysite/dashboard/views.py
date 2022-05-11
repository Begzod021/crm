from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import authenticate
from account.models import User, Employe
from account.models import Postion, AdduserCount
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from task.models import Task
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
        task_count = Task.objects.filter(employe=employe)
        employe_country = {}
        for el in Employe.COUNTRY:
            employe_country[el[0]] = Employe.get_country(el[0])
        for i in AdduserCount.objects.all():
            procent = (user_count*100)/i.users
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
 
    }
    return render(request, 'dashboard.html', context)




def get_user_country(request):
    #     ('Tashkent','Tashkent'),
    #     ('Samarkand','Samarkand'),
    #     ('Andijan','Andijan'),
    #     ('Karakalpakstan','Karakalpakstan'),
    #     ('Ferghana', 'Ferghana'),
    #     ('Bukhoro','Bukhoro'),
    #     ('Namangan', 'Namangan'),
    #     ('Khorezm', 'Khorezm'),
    #     ('Kashkadarya','Kashkadarya'),
    #     ('Jizzakh','Jizzakh'),
    #     ('Surkhandaryo','Surkhandaryo'),
    #     ('Navoi','Navoi')
    employe_tash = list(Employe.objects.filter(country="Tashkent").values())
    print(employe_tash)
    employe_Samarkand = list(Employe.objects.filter(country="Samarkand").values())
    employe_Andijan = Employe.objects.filter(country="Andijan")
    employe_Karakalpakstan = Employe.objects.filter(country="Karakalpakstan")
    employe_Ferghana = Employe.objects.filter(country="Ferghana")
    employe_Bukhoro = Employe.objects.filter(country="Bukhoro")
    employe_Namangan = Employe.objects.filter(country="Namangan")
    employe_Khorezm = Employe.objects.filter(country="Khorezm")
    employe_Kashkadarya = Employe.objects.filter(country="Kashkadarya")
    employe_Jizzakh = Employe.objects.filter(country="Jizzakh")
    employe_Surkhandaryo = Employe.objects.filter(country="Surkhandaryo")
    employe_Navoi = Employe.objects.filter(country="Navoi")

    return JsonResponse({'employe_tash':len(employe_tash)})