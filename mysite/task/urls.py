from django.urls import path, re_path

from task.views import *

urlpatterns = [
    path('calendar/<str:username>/', calendar, name='calendar' ),
    path('add_task/<str:username>', add_task, name='add_task'),
    path('update', update, name='update'),
    path('remove', remove, name='remove'),
    path('all_tasks/<str:username>', all_tasks, name='all_tasks'),
    path('task/<str:username>/', task, name='task'),
    path('delete-task/<str:username>/', delete, name='delete-task')
]