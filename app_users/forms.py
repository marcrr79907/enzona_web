from django import forms
from django.contrib.auth.forms import UserCreationForm

from app_users.models import User


class CustomUserCreationForm(UserCreationForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form_control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['username'].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = ('username', 'ci', 'phone', 'password1', 'password2')
        error_messages = {
            'username': {
                'unique': 'Ya existe un usuario con ese nombre de usuario.'
            }
        }

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
