from django.contrib import admin

from .models import Dialog_chat, Group_chat, Message


@admin.register(Dialog_chat)
class Dialog_chatAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver")
    list_display_links = ("sender", )


@admin.register(Group_chat)
class Group_chat(admin.ModelAdmin):
    list_display = ("id", "name", "link", "image", "info", "author", "created_date", "updated_date")
    list_display_links = ("name", )


@admin.register(Message)
class Message(admin.ModelAdmin):
    list_display = ("id", "message", "file", "author", "group", "dialog", "contact", "created_date")
    list_display_links = ("message", )
