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


class PositionForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['section','position', 'user', 'author']

        def __init__(self, user, **kwargs) -> None:
            super(PositionForm, self).__init__(**kwargs)
            if user:
                self.fields['section'].queryset = Employe.objects.create(user=user)



class AdminChange(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['first_name', 'last_name', 'email', 'bio','adress', 'status', 'gender','position', 'section']

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
class AddUser(forms.ModelForm):
    class Meta:
        model = AdduserCount
        fields = ['users']
        