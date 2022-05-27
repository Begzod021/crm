from django import forms
from .models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start', 'end', 'employe','creator']

        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control bdc-grey-200'
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control bdc-grey-200'
            }),
            'start':forms.DateTimeInput(attrs={
                'class':'form-control bdc-grey-200 start-date'
            }),
            'end':forms.DateTimeInput(attrs={
                'class':'form-control bdc-grey-200 end-date'
            })
        }


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start', 'end', 'status']

        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control bdc-grey-200'
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control bdc-grey-200'
            }),
            'start':forms.DateTimeInput(attrs={
                'class':'form-control bdc-grey-200 start-date'
            }),
            'end':forms.DateTimeInput(attrs={
                'class':'form-control bdc-grey-200 end-date'
            })
        }