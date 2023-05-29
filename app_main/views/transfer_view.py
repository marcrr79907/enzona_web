
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


class TranferCreateView(LoginRequiredMixin, IsSuperuserMixin, CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'transfers/transfer_create.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print(self.get_object)
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    origin = request.POST['origin_card']
                    dest = request.POST['dest_card']
                    user_card = User_Card.objects.get(user_id=request.user.id)

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
    template_name = 'cards/card_list.html'

    @ method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de transferencias'
        context['create_url'] = reverse_lazy('transfer_create')
        context['list_url'] = reverse_lazy('transfer_list')
        context['entity'] = Transfer
        context['object_list'] = Transfer.objects.all()

        return context
