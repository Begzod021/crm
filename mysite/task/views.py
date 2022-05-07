from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from account.models import *
from .models import *
from .forms import TaskEditForm, TaskForm
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='user_login')
def calendar(request, username):
    if request.user.username !=username:
        return redirect('error', username)
    else:
        user = User.objects.get(username=username)
        employes = Employe.objects.get(user=user)
        position1 = Postion.objects.get(id=employes.position.id)
        section = Section.objects.get(id=employes.section.id)
        task_count = Task.objects.filter(employe=employes).order_by('-id')
        form = TaskEditForm(request.POST or None, request.GET or None, instance=Task.objects.filter(employe=employes).first())
        if request.method == 'POST':
            form = TaskEditForm(request.POST, request.FILES, instance=Task.objects.filter(employe=employes).first())
            if form.is_valid():
                form.save()
                return redirect('calendar', request.user.username)
        context = {
            'position1':position1,
            'section':section,
            'form':form,
            'task_count':task_count,
            'employes':employes
        }
    return render(request,'calendar.html', context)


def get_tasks(request):
    user = request.user
    employee = Employe.objects.get(user=user)

    tasks = list(Task.objects.filter(employe=employee).values().order_by('-id'))

    return JsonResponse({'tasks': tasks, 'tasks_cnt': len(tasks)})



def task_detail(request):
    id = request.GET['task_id']

    task_title = Task.objects.get(id=id).title
    task_start = Task.objects.get(id=id).start
    task_end = Task.objects.get(id=id).end
    task_des = Task.objects.get(id=id).description
    print(task_title)
    return JsonResponse({'task_title': task_title, 'task_start':task_start, 'task_end':task_end, 'task_des':task_des})


@login_required(login_url='user_login')
def task(request, username):
    if request.user.username !=username:
        return redirect('error', username)
    else:
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        position1 = Postion.objects.get(id=employe.position.id)
        section = Section.objects.get(id=employe.section.id)
        task_count = Task.objects.filter(employe=employe).order_by('-id')
        form = TaskForm()
        if section.name == "CEO":
            task_users = Employe.objects.all()
            context = {
                    'position1':position1,
                    'form':form,
                    'employe':employe,
                    'task_users':task_users,
                    'section':section,
                    'task_count':task_count
            }
        else:
            task_users = Employe.objects.filter(section=employe.section.id)
            context = {
                'position1':position1,
                'form':form,
                'task_users':task_users,
                'employe':employe,
                'section':section,
                'task_count':task_count
                
            }
        if request.method == 'POST':
            form = TaskForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('task', request.user.username)
    return render(request, 'forms.html', context)



def all_tasks(request, username):

    user = User.objects.get(username=username)
    employe = Employe.objects.get(user=user)

    all_tasks = Task.objects.filter(employe=employe)
    out = []

    for task in all_tasks:
        out.append({
            'title':task.title,
            'id':task.id,
            'start':task.start,
            'end':task.end,
            'employe':str(task.employe)
        })
    
    return JsonResponse(out, safe=False)


def add_task(request, username):
    if request.method == 'GET':
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        title = request.GET.get('title')
        start = request.GET.get('start')
        end = request.GET.get('end')
        task = Task(title=str(title), start=start, end=end, employe=Employe.objects.get(user=user), creator = Employe.objects.get(user=user))
        task.save()
        data = {}
        return JsonResponse(data)

def update(request):
    start = request.GET.get('start',None)
    end = request.GET.get('end', None)
    id = request.GET.get('id', None)
    title = request.GET.get('title', None)
    task = Task.objects.get(id=id)
    task.start=start
    task.end = end
    task.title = title
    task.save()
    data={}
    return JsonResponse(data)


def delete(request, slug):
    task = Task.objects.filter(slug=slug).first()
    task.delete()
    return redirect('calendar', request.user.username)
    
