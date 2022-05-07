from django.db import models

from account.models import Employe
from contact.models import Contact


class Group_chat(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=20, unique=True, blank=True)
    image = models.ImageField(upload_to="Chat/Groups/logos/", blank=True)
    info = models.CharField(max_length=200, blank=True)
    add_members = models.BooleanField(default=True)
    
    author = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, related_name='my_groups')
    admins = models.ManyToManyField(Employe, blank=True, related_name='my_admin_groups')
    members = models.ManyToManyField(Employe, related_name='my_follow_groups')
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Dialog_chat(models.Model):
    sender = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='dialog_in_sender')
    receiver = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, related_name='dialog_in_receiver')


    def __str__(self):
        return f'{self.sender.user.username} - {self.receiver.user.username}'


class Message(models.Model):
    message = models.CharField(max_length=500, blank=True)
    file = models.FileField(upload_to='Chat/messages/files/', blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    
    author = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group_chat, on_delete=models.CASCADE, blank=True, null=True)
    dialog = models.ForeignKey(Dialog_chat, on_delete=models.CASCADE, blank=True, null=True, related_name="dialog_messages")

    created_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.author}: {self.message}"
    
    
    def time(self):
        return self.created_date.strftime('%H:%M')