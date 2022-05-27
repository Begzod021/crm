from asyncio.log import logger
from django.http import HttpResponse

from requests import request
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import shared_task
import requests
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from task.models import Task
import json
from celery import Celery, states
from celery.exceptions import Ignore
import asyncio
from account.views import employe
from .weather import weather_get
logger = get_task_logger(__name__)



@shared_task
@periodic_task(run_every=(crontab(minute='*/15')), name='get_weather', ignore_result=True)
def get_weather():
   
   print(True)


@shared_task(bind = True)
@periodic_task(run_every=(crontab(minute='*/15')), name='broadcast_notification', ignore_result=True)
def broadcast_notification():
        notification = Task.objects.all()

        if len(notification) > 0:
            notification = notification.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "notification_broadcast",
                {
                    'type':'send notification',
                    'message':json.dumps(notification.message),
                }
            ))

            notification.active = True
            notification.save()

            return 'Done'
