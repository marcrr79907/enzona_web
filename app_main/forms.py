from django.forms import ModelForm
from .models import *
from django import forms


class CardForm(ModelForm):

    class Meta:
        model = User_Card
        fields = ['card_number', 'pin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form_control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['card_number'].widget.attrs['autofocus'] = True

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


class TransferForm(ModelForm):

    class Meta:
        model = Transfer
        fields = ['origin_card', 'dest_card',
                  'import_transfer']
        

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


class ServiceForm(ModelForm):

    class Meta:
        model = Service_Pay
        fields = ['service_id', 'service_type',
                  'propietary']

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


class ServicePayForm(ModelForm):

    class Meta:
        model = Service_Pay
        fields = []

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


class DestinataryForm(ModelForm):

    class Meta:
        model = Destinatary
        fields = ['name', 'associated_card']
        

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
