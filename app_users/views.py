from django.http import JsonResponse
from app_main.models import Person_DB, Phone_DB
from app_users.models import User
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
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
        context['title'] = 'Bienvenido'
        return context


class RegisterView(CreateView):

    model = User
    form_class = CustomUserCreationForm
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    try:
                        dni = request.POST['ci']
                        phone_number = request.POST['phone']

                        person = Person_DB.objects.get(dni=dni)
                        phone = Phone_DB.objects.get(number=phone_number)

                        if not person.register and not phone.associated:
                            if request.POST['password'] == request.POST['password2']:

                                data = form.save()
                            else:
                                data['error'] = 'Los campos de contraseña no coinciden!'
                        else:
                            data['error'] = 'Carnet de identidad o teléfono ya en uso!'

                    except Exception as e:
                        data['error'] = str(e)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar '
        context['entity'] = 'User'
        context['list_url'] = reverse_lazy('signup')
        context['action'] = 'add'

        return context
