from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.core.cache import cache
import datetime
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from .enums import UserRole
from .manager import *
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class User(AbstractUser):
    slug = models.SlugField(blank=True)
    has_profile = models.BooleanField(default=False)
    remember_me = models.BooleanField(default=False)
    role = models.CharField(max_length=35, choices=UserRole.choices(), null=True)
    approve = models.BooleanField(default=False)



    def has_profile_true(self):
        self.has_profile = True


    def has_profile_false(self):
        self.has_profile = False


    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class Section(models.Model):

    section_type = (
        ('',''),
        ('CEO','CEO'),
        ('Agent','Agent'),
        ('Manager-dispatcher','Manager-dispatcher'),
        ('Accountant','Accountant'),
        ('Sales Manager','Sales Manager'),
        ('Office Manager','Office Manager'),
    )


    name = models.CharField(max_length=250, null=True, choices=section_type, default=False)
    section = models.ForeignKey('Section', on_delete=models.PROTECT, related_name='sections', null=True, blank=True)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Postion(models.Model):
    
    type =(

        ('',''),
        ('director','director'),
        ('deputy','deputy'),
        ('worker','worker'),
    )


    position = models.CharField(max_length=250, choices=type, null=True, default=False)
    description = models.CharField(max_length=250, null=True)
    task = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.position



class Email(models.Model):
    email = models.EmailField(max_length=250, blank=True, null=True)
    author = models.ForeignKey(User, models.CASCADE, related_name='authors', blank=True, null=True)
    slug = models.SlugField()


    def __str__(self) -> str:
        return self.email


    def save(self, *args, **kwargs):
        self.slug = slugify(self.email)

        return super().save(*args, **kwargs)


class Employe(models.Model):
    choice = (
        ('Not specified','Not specified'),
        ('Male','Male'),
        ('Female','Female'),
    )
    COUNTRY = (
        ('Tashkent','Tashkent'),
        ('Samarkand','Samarkand'),
        ('Andijan','Andijan'),
        ('Nukus','Nukus'),
        ('Ferghana', 'Ferghana'),
        ('Bukhara','Bukhara'),
        ('Namangan', 'Namangan'),
        ('Urganch', 'Urganch'),
        ('Qarshi','Qarshi'),
        ('Jizzakh','Jizzakh'),
        ('Termiz','Termiz'),
        ('Navoiy','Navoiy'),
        ('Sirdaryo','Sirdaryo'),

    )

    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    position = models.ForeignKey(Postion, on_delete=models.PROTECT, related_name="model_position")
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name='task_section')
    slug = models.SlugField()
    author = models.ForeignKey('self', on_delete=models.SET_NULL,null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=150, choices=choice, blank=True, null=True, default=choice[0][0])
    bio = models.TextField(null=True, blank=True)
    adress = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    email_add = models.ManyToManyField(Email)
    country = models.CharField(max_length=120, choices=COUNTRY, blank=True, null=True)
    is_online = models.BooleanField(default = False)
    email = models.EmailField(max_length=150, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)

    def get_country(el):
        return Employe.objects.filter(country=el).count()


    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)

        return super().save(*args, **kwargs)




    def __str__(self) -> str:
        return str(self.user)




class AdduserCount(models.Model):
    users = models.PositiveIntegerField()


class ChatSession(models.Model):
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user1_name')
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user2_name')
    updated_on = models.DateTimeField(auto_now = True)
    
    class Meta:
        unique_together = (("user1", "user2"))
        verbose_name = 'Chat Message'
        
    def __str__(self):
        return '%s_%s' %(self.user1.username,self.user2.username)
        
    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    @staticmethod
    def chat_session_exists(user1,user2):
        return ChatSession.objects.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)).first()
    
    @staticmethod
    def create_if_not_exists(user1,user2):
        res = ChatSession.chat_session_exists(user1,user2)
        return False if res else ChatSession.objects.create(user1=user1,user2=user2)

class Admin(User):
    objects =  AdminManager()

    class Meta:
        proxy = True



class Director(User):
    objects = DirectorManager()


    class Meta:
        proxy = True

class Deputy(User):
    objects = DeputyManager


    class Meta:
        proxy = True

class Worker(User):
    objects = WorkerManager() 


    class Meta:
        proxy = True




