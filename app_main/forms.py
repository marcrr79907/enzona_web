from django.forms import ModelForm
from django.http import HttpResponse
from .models import *
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


class CardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form_control'
            form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = User_Card
        fields = ['card_number', 'pin']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return data
