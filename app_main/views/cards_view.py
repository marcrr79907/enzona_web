from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from ..models import *
from ..forms import *


class CardListView(ListView):
    model = User_Card
    template_name = 'cards/cards_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de tarjetas'
        context['object_list'] = User_Card.objects.all()

        return context


class CardCreateView(CreateView):
    model = User_Card
    form_class = CardForm
    template_name = 'cards/card_create.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opcción'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Tarjeta'
        context['entity'] = 'User_Card'
        context['list_url'] = reverse_lazy('app_main:card_create')
        context['action'] = 'add'

        return context


class CardUpdateView(UpdateView):
    model = User_Card
    form_class = CardForm
    template_name = 'cards/cards.html'
    success_url = reverse_lazy('cards/cards_list')
