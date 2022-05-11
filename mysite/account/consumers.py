from channels.generic.websocket import AsyncWebsocketConsumer, AsyncConsumer
import json
from datetime import datetime
from channels.db import database_sync_to_async
import uuid
from .models import  Employe,ChatSession
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

class PersonalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'personal__{self.room_name}'
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        if self.scope["user"].is_authenticated:
            await self.accept()
        else:
            await self.close(code=4001)
            
    async def disconnect(self, code):
        self.set_offline()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('msg_type')
        user_id = data.get('user_id')
        
        if msg_type == MESSAGE_TYPE['WENT_ONLINE']:
            users_room_id = await self.set_online(user_id)
            for room_id in users_room_id:
                await self.channel_layer.group_send(
                    f'personal__{room_id}',
                    {
                    'type': 'user_online',
                    'user_name' : self.user.username
                    }
                )
        elif msg_type == MESSAGE_TYPE['WENT_OFFLINE']:
            users_room_id = await self.set_offline(user_id)
            for room_id in users_room_id:
                await self.channel_layer.group_send(
                    f'personal__{room_id}',
                    {
                    'type': 'user_offline',
                    'user_name' : self.user.username
                    }
                )
            
    async def user_online(self,event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['WENT_ONLINE'],
            'user_name' : event['user_name']
        }))
        
    async def message_counter(self, event):
        overall_unread_msg = await self.count_unread_overall_msg(event['current_user_id'])
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['MESSAGE_COUNTER'],
            'user_id': event['user_id'],
            'overall_unread_msg' : overall_unread_msg
        }))

    async def user_offline(self,event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['WENT_OFFLINE'],
            'user_name' : event['user_name']
        }))
    
    @database_sync_to_async
    def set_online(self,user_id):
        Employe.objects.filter(user__id = user_id).update(is_online = True)
        user_all_friends = ChatSession.objects.filter(Q(user1 = self.user) | Q(user2 = self.user))
        user_id = []
        for ch_session in user_all_friends:
            user_id.append(ch_session.user2.id) if self.user.username == ch_session.user1.username else user_id.append(ch_session.user1.id)
        return user_id

    @database_sync_to_async
    def set_offline(self,user_id):
        Employe.objects.filter(user__id = user_id).update(is_online = False)
        user_all_friends = ChatSession.objects.filter(Q(user1 = self.user) | Q(user2 = self.user))
        user_id = []
        for ch_session in user_all_friends:
            user_id.append(ch_session.user2.id) if self.user.username == ch_session.user1.username else user_id.append(ch_session.user1.id)
        return user_id
    