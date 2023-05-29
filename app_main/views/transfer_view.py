
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from ..mixins import IsSuperuserMixin
from ..models import *
from ..forms import *


class TranferCreateView(LoginRequiredMixin, CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'transferencia/transferencias.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    origin = request.POST['origin_card']
                    dest = request.POST['dest_card']
                    mont = request.POST['import_transfer']
                    user_card = User_Card.objects.get(
                        user=request.user.id, card_number=origin)
                    dest_card = User_Card.objects.get(card_number=dest)

                    if mont <= 0:
                        if user_card.balance >= mont:
                            dest_card.balance += mont
                            user_card.balance -= mont
                            user_card.save()

                        else:
                            data['error'] = 'Saldo insuficiente'
                    else:
                        data['error'] = 'El saldo a transferir no puede ser cero'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Tarjeta'
        context['entity'] = 'Transfer'
        context['list_url'] = reverse_lazy('transfer_create')
        context['action'] = 'add'

        return context


class CardListView(LoginRequiredMixin, ListView):
    model = User_Card
    template_name = 'transferencias/transferencias.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de transferencias'
        context['create_url'] = reverse_lazy('transfer_create')
        context['list_url'] = reverse_lazy('transferencias')
        context['entity'] = Transfer
        context['object_list'] = Transfer.objects.filter(id=self.request.user)

        return context
