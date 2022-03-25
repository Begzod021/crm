from django.db import models
from django.utils.text import slugify
# Create your models here.
from account.models import *
class Task(models.Model):

    choice = (
        ('',''),
        ('completed','completed'),
        ('not completed','not completed'),
    )



    employe = models.ManyToManyField(Employe, blank=True)
    creator = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='creators')
    checker = models.ManyToManyField(Employe, related_name='checkers')
    active = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True)
    starteddate = models.DateTimeField(blank=True)
    upload = models.DateTimeField(blank=True)
    section = models.ManyToManyField(Section)
    status = models.CharField(max_length=100, choices=choice, default=False, blank=True)
    name = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField()
    file = models.FileField(upload_to='files/', blank=True, null=True)
    image = models.ImageField(upload_to='task_images/', blank=True, null=True)


    def save(self, *args, **kwargs):
        
        slug = f'{self.name}'


        self.slug = slugify(slug)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return str(self.creator)
