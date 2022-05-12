import imp
from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['id', 'username']

@admin.register(Postion)
class AdminPosition(admin.ModelAdmin):
    list_display = ['id', 'author', 'position']

@admin.register(Section)
class AdminSection(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Employe)
class AdminProfile(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(Email)
class AdminEmail(admin.ModelAdmin):
    list_display = ['id', 'email']

@admin.register(AdduserCount)
class AdminCountUser(admin.ModelAdmin):
    list_display = ['id', 'users']


@admin.register(ChatSession)
class AdminCountUser(admin.ModelAdmin):
    list_display = ['user1', 'user2']

