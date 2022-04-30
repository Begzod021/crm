from django import forms
from .models import *

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start', 'end', 'employe']

        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control bdc-grey-200'
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control bdc-grey-200'
            }),
            'start':forms.TextInput(attrs={
                'class':'form-control bdc-grey-200 start-date'
            }),
            'end':forms.TextInput(attrs={
                'class':'form-control bdc-grey-200 end-date'
            })
        }