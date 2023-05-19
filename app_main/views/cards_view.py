from typing import Any
from django import http
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from ..models import *
from ..forms import *


class CardListView(ListView):
    model = User_Card
    template_name = 'cards/card_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de tarjetas'
        context['object_list'] = User_Card.objects.all()

        return context


class CardCreateView(CreateView):
    model = User_Card
    form_class = CardForm
    template_name = 'cards/card_create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def post(self, request, *args, **kwargs):
        data = {}
        print(self.get_object)
        try:
            action = request.POST['action']
            if action == 'add':
                form = CardForm(request.POST)

                if form.is_valid():
                    card = Bank_DB.objects.get(
                        card_number=request.POST['card_number'])
                    if not card.associated:
                        if request.POST['pin'] == card.pin:

                            data = form.save()
                            print(form)
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


class CardUpdateView(UpdateView):
    model = User_Card
    form_class = CardForm
    template_name = 'cards/card_create.html'
    success_url = reverse_lazy('cards/cards_list')

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
        context['list_url'] = reverse_lazy('card_edit')
        context['action'] = 'edit'

        return context


class CardDeleteView(DeleteView):
    model = User_Card
    template_name = 'cards/card_delete.html'
    success_url = reverse_lazy('card_delete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Tarjeta'
        context['entity'] = 'User_Card'
        context['list_url'] = reverse_lazy('card_delete')

        return context
