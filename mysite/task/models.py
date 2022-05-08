from operator import mod
from django.db import models
from django.utils.text import slugify
# Create your models here.
from account.models import *
class Task(models.Model):

    choice = (
        ('',''),
        ('in progress','in progress'),
        ('completed','completed'),
        ('not completed','not completed'),
    )



    employe = models.ForeignKey(Employe,on_delete=models.CASCADE, blank=True, null=True)
    creator = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='creators', blank=True, null=True)
    checker = models.ManyToManyField(Employe, related_name='checkers')
    active = models.BooleanField(default=False)
    end = models.DateTimeField(null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    upload = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)
    title = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    file = models.FileField(upload_to='files/', blank=True, null=True)
    image = models.ImageField(upload_to='task_images/', blank=True, null=True)
    id = models.AutoField(primary_key=True)

    def save(self, *args, **kwargs):
        
        slug = f'{self.title}'


        self.slug = slugify(slug)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return str(self.creator)
