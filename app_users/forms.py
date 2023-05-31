from django import forms
from django.contrib.auth.forms import UserCreationForm

from app_users.models import User


class CustomUserCreationForm(UserCreationForm):
    password2 = forms.CharField(widget=forms.PasswordInput)

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


class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username','phone')
        error_messages = {
            'username': {
                'unique': 'Ya existe un usuario con ese nombre de usuario.'
            },
            'phone': {
                'unique': 'Ya existe un usuario con ese telefono.'
            }
        }
         
    # Manejo de usuario y modificacion de password
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.changed_data['password1']
                u = form.save(commit=False)

                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()

            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return data
