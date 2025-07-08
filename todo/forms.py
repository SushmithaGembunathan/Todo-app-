from django.contrib.auth.models import User
from django import forms
from .models import Task

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }