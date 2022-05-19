from asyncio.log import logger
from django.http import HttpResponse

from requests import request
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery import shared_task
import requests
from datetime import datetime

from account.views import employe
from .weather import weather_get
logger = get_task_logger(__name__)



@shared_task
@periodic_task(run_every=(crontab(minute='*/15')), name='get_weather', ignore_result=True)
def get_weather():
   
   weather_get()
   weather = weather_get()
   context = {
       'weather':weather
   }
   return context