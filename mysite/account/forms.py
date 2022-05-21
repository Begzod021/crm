from email.policy import default
from tkinter import Widget
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class AddAdmin(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username','password', 'remember_me', 'email']

        widgets = {
            'username':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your username'
            }),
            'password':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your password',
                'type':'password',
                'name':'password',
                'id':'password',
                'aria-describedby':'password'
            }),
            'remember_me':forms.CheckboxInput(attrs={
                'class':'form-check-input'
            }),
            'email':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your email',
                'type':'email'
    }),
         }

class PositionForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['section','position', 'user', 'author', 'country']

        def __init__(self, user, **kwargs) -> None:
            super(PositionForm, self).__init__(**kwargs)
            if user:
                self.fields['section'].queryset = Employe.objects.create(user=user)



class AdminChange(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['first_name', 'last_name', 'email', 'bio', 'gender','position', 'section', 'country']

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
            'gender':forms.Select(attrs={
                'class':'form-control'
            }),
            'position':forms.Select(attrs={
                'class':'form-control'
            }),
            'section':forms.Select(attrs={
                'class':'form-control'
            }),
            'user':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'country':forms.Select(attrs={
                'class':'form-control'
            }),
        }
class AddUser(forms.ModelForm):
    class Meta:
        model = AdduserCount
        fields = ['users']

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget = forms.EmailInput(attrs={"class": "form-control"})