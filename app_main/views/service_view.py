from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from ..models import *
from ..forms import *


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service_Pay
    template_name = 'servicios/servicios.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        services_list = Service_Pay.objects.filter(user=self.request.user)

        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Mis Servicios'
        context['title'] = 'Agregar Servicio'
        context['entity'] = Service_Pay
        context['object_list'] = services_list
        context['action'] = 'add'

        return context

