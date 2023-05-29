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

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cards_list = User_Card.objects.filter(
            user=self.request.user)
        cards = []
        for c in cards_list:
            try:
                cards.append(Bank_DB.objects.get(card_number=c.card_number))
            except:
                pass

        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de tarjetas'
        context['create_url'] = reverse_lazy('card_create')
        context['list_url'] = reverse_lazy('card_list')
        context['entity'] = User_Card
        context['object_list'] = cards

        return context


class CardCreateView(LoginRequiredMixin, CreateView):
    model = User_Card
    form_class = CardForm
    template_name = 'card/credit_card.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    card = Bank_DB.objects.get(
                        card_number=request.POST['card_number'])
                    if not card.associated:
                        if request.POST['pin'] == card.pin:
                            form.instance.user = self.request.user
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


class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = User_Card
    template_name = 'card/credit_card.html'
    success_url = reverse_lazy('card_create')


class CardFormView(FormView):
    form_class = CardForm
    template_name = 'cards/credit_card.html'
    success_url = reverse_lazy('card_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario Tarjeta'
        context['entity'] = 'User_Card'
        context['list_url'] = reverse_lazy('card_list')
        context['action'] = 'add'

        return context
