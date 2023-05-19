from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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
        self.fields['date_ex'].widget = forms.HiddenInput()
        self.fields['currency_type'].widget = forms.HiddenInput()

    class Meta:
        model = User_Card
        fields = ['card_number', 'pin', 'date_ex', 'currency_type']

    def save(self, commit=True):
        data = {}
        form = super().save(commit=False)
        number = self.cleaned_data.get('card_number')
        if number:
            # Obtiene el objeto existente
            card = get_object_or_404(Bank_DB, card_number=number)
            form.date_ex = card.date_exp
            form.currency_type = card.currency_type

        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return data
