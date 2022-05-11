from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from .models import ChatSession,Employe, User
from django.core.exceptions import ValidationError

@receiver(post_save,sender=ChatSession)
def sender_receiver_no_same(sender,instance,created,**kwargs):
    if created:
        if instance.user1 == instance.user2:
            raise ValidationError("Sender and Receiver are not same!!",code='Invalid')

@receiver(post_save,sender=User)
def at_ending_save(sender,instance,created,**kwargs):
    if created:
        # UserChat.objects.create(user = instance)
        Employe.objects.create(user = instance)

