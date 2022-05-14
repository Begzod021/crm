from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from account.models import *
from task.serializers import TaskSerializers
from .models import *
from .forms import TaskEditForm, TaskForm
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
        tasks = Task.objects.all()
        count_todos = task_count.count()
        completed_todo = Task.objects.filter(status=True, employe=employes).order_by('-id')
        count_completed_todo = completed_todo.count()
        uncompleted = count_todos - count_completed_todo
        context = {
            'position1':position1,
            'section':section,
            'task_count':task_count,
            'employes':employes,
            'tasks':tasks,
            'count_todos':count_todos,
            'count_completed_todo':count_completed_todo,
            'uncompleted':uncompleted
        }
    return render(request,'calendar.html', context)



@api_view(['GET'])
def allTask(request):
    tasks = Task.objects.all()
    serializer = TaskSerializers(tasks, data=request.data)

    return Response(serializer.data)


@api_view(['GET'])
def detailTask(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializers(task, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


class TaskUpdate(generics.RetrieveUpdateAPIView):
    def patch(self, request, pk):
        task = Task.objects.get(id=pk)
        serializer = TaskSerializers(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    












def get_tasks(request):
    user = request.user
    employee = Employe.objects.get(user=user)

    tasks = list(Task.objects.filter(employe=employee).values().order_by('-id'))
    task_completed = list(Task.objects.filter(status=True, employe=employee).values())
    uncompleted = len(tasks) - len(task_completed)
    return JsonResponse({'tasks': tasks, 'tasks_cnt': len(tasks), 
    'task_completed':len(task_completed), 'uncompleted':uncompleted,})






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
            task_list = Task.objects.filter(creator=employe)
            context = {
                    'position1':position1,
                    'form':form,
                    'employe':employe,
                    'task_users':task_users,
                    'section':section,
                    'task_count':task_count,
                    'task_list':task_list
            }
        else:
            task_users = Employe.objects.filter(section=employe.section.id)
            task_list = Task.objects.filter(creator=employe)
            context = {
                'position1':position1,
                'form':form,
                'task_users':task_users,
                'employe':employe,
                'section':section,
                'task_count':task_count,
                'task_list':task_list
                
            }
        if request.method == 'POST':
            form = TaskForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('task', request.user.username)
    return render(request, 'forms.html', context)


def update_task(request, pk, username):
    if request.user.username !=username:
        return redirect('error', username)
    else:
        user = User.objects.get(username=username)
        employe = Employe.objects.get(user=user)
        position1 = Postion.objects.get(id=employe.position.id)
        section = Section.objects.get(id=employe.section.id)
        task_count = Task.objects.filter(employe=employe).order_by('-id')
        form = TaskEditForm(request.POST or None, request.FILES or None, instance=Task.objects.get(id=pk))
        if request.method == 'POST':
            form = TaskEditForm(request.POST, instance=Task.objects.get(id=pk))
            if form.is_valid():
                form.save()
                return redirect('calendar', request.user.username)
    context = {
            'form':form,
            'position1':position1,
            'section':section,
            'task_count':task_count,
            'employe':employe
        }
    return render(request, 'update-task.html', context)



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
    
