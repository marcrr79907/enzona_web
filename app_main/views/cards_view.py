
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from ..models import *
from ..forms import *


class CardListView(LoginRequiredMixin, ListView):
    model = User_Card
    template_name = 'card/credit_card.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cards_list = User_Card.objects.filter(
            user=self.request.user)

        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Mis Tarjetas'
        context['title'] = 'Agregar Tarjeta'
        context['entity'] = User_Card
        context['object_list'] = cards_list
        context['action'] = 'add'

        return context


class CardCreateView(LoginRequiredMixin, CreateView):
    model = User_Card
    form_class = CardForm
    template_name = 'card/credit_card.html'
    success_url = reverse_lazy('system:card_list')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    card = Bank_DB.objects.get(
                        card_number=request.POST['card_number'])
                    if not card.associated:
                        if request.POST['pin'] == card.pin:
                            form.instance.user = self.request.user
                            form.instance.bank_type = card.bank_type
                            form.instance.currency_type = card.currency_type
                            card.associated = True

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

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'User_Card'
        context['list_url'] = reverse_lazy('card_create')

        return context


class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = User_Card
    success_url = reverse_lazy('system:card_list')
    template_name = 'card/eliminar_card.html'
