from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from ..models import *
from ..forms import *


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service_Pay
    form_class = ServiceForm
    template_name = 'servicios/servicios.html'
    success_url = reverse_lazy('system:service_list')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        global success_url

        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    service_type = request.POST['service_type']
                    id = request.POST['service_id']
                    if service_type == 'electricidad':
                        service = Electricity_Service.objects.get(
                            electricity_id=id)
                        form.instance.user = self.request.user
                        form.instance.import_service = service.electricity_cost

                    else:
                        service = Gas_Service.objects.get(gas_id=id)
                        form.instance.user = self.request.user
                        form.instance.import_service = service.gas_cost

                    data = form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        except Exception as e:
            data['error'] = str(e)

        return redirect(success_url, {
            'data': data
        })

    def get_context_data(self, **kwargs):
        cards_list = User_Card.objects.filter(
            user=self.request.user)

        context = super().get_context_data(**kwargs)
        context['object_list'] = cards_list
        context['action'] = 'add'

        return context


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service_Pay
    success_url = reverse_lazy('system:service_list')
    template_name = 'card/eliminar.html'


class ServiceUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    form_class = ServiceUpdateForm
    template_name = 'servicios/servicios.html'
    success_url = reverse_lazy('system:service_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        global success_url

        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    user_card = User_Card.objects.get(
                        card_number=request.POST['card_number'])
                    service = self.object
                    if user_card.balance >= service.import_service:

                        user_card -= service.import_service
                        service.checked = True
                        user_card.save()
                        service.save()
                        form.save()

                    else:
                        data['error'] = 'Saldo insuficiente para realizar la operación'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'Noha ingresado ninguna acción'
        except Exception as e:
            data['error'] = str(e)

        return redirect(success_url, {
            'data': data
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pagar Servicio'
        context['action'] = 'edit'

        return context
