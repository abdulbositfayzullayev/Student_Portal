from django import forms
from .models import Homework,Todo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = '__all__'

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label='Bu yerdan izlashingiz mumkin')


class SignupCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


