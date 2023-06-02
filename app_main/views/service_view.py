from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from ..models import *
from ..forms import *


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service_Pay
    template_name = 'servicios/servicios.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        services_tbp = Service_Pay.objects.filter(
            user=self.request.user, checked=False)
        # Historial
        paid_services = Service_Pay.objects.filter(
            user=self.request.user, checked=True)

        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Mis Servicios'
        context['title'] = 'Agregar Servicio'
        context['entity'] = Service_Pay
        context['services_tbp'] = services_tbp
        # Historial
        context['paid_services'] = paid_services
        context['action'] = 'add'

        return context


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


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service_Pay
    success_url = reverse_lazy('system:service_list')
    template_name = 'delete.html'


class ServicePayView(LoginRequiredMixin, UpdateView):

    model = Service_Pay
    form_class = ServicePayForm
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
            if action == 'pay':
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
        user_cards = User_Card.objects.filter(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pagar Servicio'
        context['action'] = 'pay'
        context['cards_list'] = user_cards

        return context


class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service_Pay
    form_class = ServiceForm
    template_name = 'servicios/servicios.html'
    success_url = reverse_lazy('system:service_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        global url_redirect

        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'edit':
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

        return redirect(url_redirect, {
            'data': data
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_edit'] = 'Editar Servicio'
        context['action'] = 'edit'

        return context
