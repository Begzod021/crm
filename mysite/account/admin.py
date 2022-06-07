from atexit import register
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



@admin.register(AdduserCount)
class AdminCountUser(admin.ModelAdmin):
    list_display = ['id', 'users']

admin.site.register(Admin)
admin.site.register(Director)
admin.site.register(Deputy)
admin.site.register(Worker)