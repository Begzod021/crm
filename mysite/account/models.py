

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
# Create your models here.


class User(AbstractUser):
    slug = models.SlugField()



    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username



class Section(models.Model):
    name = models.CharField(max_length=250, null=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='sections', null=True, blank=True)
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
        ('chief','chief'),
        ('deputy','deputy'),
        ('worker','worker'),
    )


    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    position = models.CharField(max_length=250, choices=type, null=True, default=False)
    description = models.CharField(max_length=250, null=True)
    task = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.position


class Employe(models.Model):


    choice = (
        ('',''),
        ('Male','Male'),
        ('Female','Female'),
    )


    
    position = models.ForeignKey(Postion, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    slug = models.SlugField()
    author = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=150, choices=choice, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    adress = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)




    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)

        return super().save(*args, **kwargs)




    def __str__(self) -> str:
        return str(self.user)