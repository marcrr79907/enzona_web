from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from app_main.models import Person_DB, Phone_DB
from app_users.models import User
from .forms import CustomUserCreationForm, UserUpdateForm
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from project_EZ import settings


class UsersLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ingrese usuario y contraseña'
        return context

class RegisterView(CreateView):

    model = User
    form_class = CustomUserCreationForm
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()

                if form.is_valid():

                    dni = request.POST['ci']
                    phone_number = request.POST['phone']

                    person = Person_DB.objects.get(dni=dni)
                    phone = Phone_DB.objects.get(number=phone_number)

                    if not person.register and not phone.associated:
                        if request.POST['password1'] == request.POST['password2']:
                            person.register = True
                            phone.associated = True

                            data = form.save()

                        else:
                            data['error'] = 'Los campos de contraseña no coinciden!'
                    else:
                        data['error'] = 'Carnet de identidad o teléfono ya en uso!'

                else:
                    data['error'] = form.errors

            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        except Exception as e:
            data['error'] = str(e)

        return redirect(settings.LOGIN_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crea una cuenta'
        context['entity'] = 'User'
        context['list_url'] = reverse_lazy('register')
        context['action'] = 'add'

        return context
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'editp.html'
    success_url = reverse_lazy('users:profile')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                phone = Phone_DB.objects.get(number=request.POST['phone'])
                print(request.POST['phone'])
                if form.is_valid():
                    if phone:
                        data = form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción'
        except Exception as e:
            data['error'] = str(e)

        return redirect('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar usuario'
        context['action'] = 'edit'

        return context    

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        data_user = Person_DB.objects.get(dni=user.ci)

        context = super().get_context_data(**kwargs)
        context['data_user'] = data_user
        context['user'] = user

        return context   

class SegurityView(LoginRequiredMixin, TemplateView):
    template_name = 'segurity.html' 
   
