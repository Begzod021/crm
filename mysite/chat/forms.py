from dataclasses import fields
from .models import Message
from django import forms


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("message", "file", "contact", "author", "group", "dialog" )
