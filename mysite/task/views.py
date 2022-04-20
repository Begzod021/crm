from asyncio.base_tasks import _task_get_stack
from django.http import JsonResponse
from django.shortcuts import render, redirect
from account.models import *
from .models import *
from .forms import TaskForm
# Create your views here.
def calendar(request, username):
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
            tasks = Task.objects.all()
            form = TaskForm()
            section = Section.objects.get(id=employe.section.id)
            if section.name == "CEO":
                task_users = Task.objects.all()
                context = {
                        'position1':position1,
                        'form':form,
                }
            else:
                task = Task.objects.filter(section=employe.section.id).first()
                task_users = Employe.objects.filter(section=employe.section.id)
                context = {
                    'task':task,
                    'position1':position1,
                    'form':form,
                    'task_users':task_users,
                }
            if request.method == 'POST':
                form = TaskForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    return redirect('calendar', request.user.username)
    return render(request,'calendar.html', context)

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

def add_task(request):
    title = request.GET.get('title', None)
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    id = request.GET.get('id', None)
    task = Task(title=str(title),start=start, end=end, id=id)
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

def remove(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(id=id)
    task.delete()
    data = {}
    return JsonResponse(data)
