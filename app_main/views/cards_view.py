from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from ..models import *
from ..forms import *


class CardListView(LoginRequiredMixin, ListView):
    model = User_Card
    template_name = 'card/credit_card.html'

    @ method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de tarjetas'
        context['create_url'] = reverse_lazy('card_create')
        context['list_url'] = reverse_lazy('card_list')
        context['entity'] = User_Card
        context['object_list'] = User_Card.objects.all()

        return context


class CardCreateView(LoginRequiredMixin, CreateView):
    model = User_Card
    form_class = CardForm
    template_name = 'card/credit_card.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user_id = self.request.user

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        data = {}
        print(self.get_object)
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    card = Bank_DB.objects.get(
                        card_number=request.POST['card_number'])
                    if not card.associated:
                        if request.POST['pin'] == card.pin:
                            data = form.save()
                        else:
                            data['error'] = 'Pin incorrecto'
                    else:
                        data['error'] = 'La tarjeta ya está asociada a un usuario!'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Tarjeta'
        context['entity'] = 'User_Card'
        context['list_url'] = reverse_lazy('card_create')
        context['action'] = 'add'

        return context


class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = User_Card
    form_class = CardForm
    template_name = 'card/credit_card.html'
    success_url = reverse_lazy('card_update')

    @ method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tarjeta'
        context['entity'] = 'User_Card'
        context['list_url'] = reverse_lazy('card_update')
        context['action'] = 'edit'

        return context


class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = User_Card
    template_name = 'card/credit_card.html'
    success_url = reverse_lazy('card_delete')

    @ method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args: str, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Tarjeta'
        context['entity'] = 'User_Card'
        context['list_url'] = reverse_lazy('card_delete')

        return context


class CardFormView(FormView):
    form_class = CardForm
    template_name = 'cards/card_create.html'
    success_url = reverse_lazy('card_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario Tarjeta'
        context['entity'] = 'User_Card'
        context['list_url'] = reverse_lazy('card_list')
        context['action'] = 'add'

        return context
