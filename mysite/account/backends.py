from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.backends import BaseBackend

class MyBackend(BaseBackend):

    def get_user(self, user_id):
        try:
            users = get_user_model().objects.get(pk=user_id)
            users.last_online = timezone.now() 
            users.save(update_fields=['last_online'])
            return users
        except get_user_model().DoesNotExist:
            return None