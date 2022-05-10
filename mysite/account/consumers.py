from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime
from channels.db import database_sync_to_async
import uuid
from .models import User, Employe
from django.db.models import Q





MESSAGE_TYPE = {
    "WENT_ONLINE": 'WENT_ONLINE',
    "WENT_OFFLINE": 'WENT_OFFLINE',
    "IS_TYPING": 'IS_TYPING',
    "NOT_TYPING": 'NOT_TYPING',
    "MESSAGE_COUNTER": 'MESSAGE_COUNTER',
    "OVERALL_MESSAGE_COUNTER": 'OVERALL_MESSAGE_COUNTER',
    "TEXT_MESSAGE": 'TEXT_MESSAGE',
    "MESSAGE_READ": 'MESSAGE_READ',
    "ALL_MESSAGE_READ": 'ALL_MESSAGE_READ',
    "ERROR_OCCURED": 'ERROR_OCCURED'
}



@database_sync_to_async
def update_user_status(self, user, device_id, status):
    return Employe.objects.get_or_create(
        user=user, device_id=device_id,
    ).update(status=status)