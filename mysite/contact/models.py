from account.models import Employe
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    add_contact = models.ForeignKey(Employe, on_delete=models.CASCADE)
    add_contact_to = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="my_contacts")

    
    def __str__(self):
        return f'{self.name} {self.last_name}'
    