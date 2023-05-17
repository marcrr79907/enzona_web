from django.forms import ModelForm
from .models import User
from django import forms


class CustomUserCreationForm(ModelForm):
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['user_name', 'ci', 'phone', 'password', 'password2']


class UserLogin(ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'password']
