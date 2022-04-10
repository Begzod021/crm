from tkinter import Widget
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class AddAdmin(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

        widgets = {
            'username':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Username'
            }),
            'password':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Password',
                'type':'password',
                'name':'password',
                'id':'password',
            }),
        }

class AdminChange(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['first_name', 'last_name', 'email', 'bio','adress', 'status', 'gender']

        widgets = {
            'first_name':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'last_name':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'email':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'bio':forms.Textarea(attrs={
                'class':'form-control',
                'type':'text',
                'name':'text'
            }),
            'adress':forms.TextInput(attrs={
                'class':'form-control'
            }),
        }