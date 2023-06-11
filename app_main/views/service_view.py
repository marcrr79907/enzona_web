from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from ..models import *
from ..forms import *


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service_Pay
    template_name = 'servicios/servicios.html'

    def get_context_data(self, **kwargs):
        services_tbp = Service_Pay.objects.filter(
            user=self.request.user, checked=False)
        cards_list = User_Card.objects.filter(user=self.request.user)

        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Mis Servicios'
        context['title'] = 'Agregar Servicio'
        context['entity'] = Service_Pay
        context['services_tbp'] = services_tbp
        context['cards_list'] = cards_list
        context['action'] = 'add'
        context['action_update'] = 'edit'
        context['data'] = self.request.session.pop('data', None)
        context['action_service'] = 'pay'
        
        return context


class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service_Pay
    form_class = ServiceForm
    template_name = 'servicios/servicios.html'
    success_url = reverse_lazy('system:service_list')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        data['form_is_valid'] = False
        try:
            action = request.POST['action']
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
                    
                    form.save()
                    data['form_is_valid'] = True
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        
        except Gas_Service.DoesNotExist:
            data['error'] = 'El servicio no existe!'
        except Electricity_Service.DoesNotExist:
            data['error'] = 'El servicio no existe!'
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'El servicio ha sido creado con éxito.'}
            print(request.session['data'])
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            print(request.session['data'])
            return redirect(self.success_url)


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service_Pay
    success_url = reverse_lazy('system:service_list')
    template_name = 'eliminar.html'

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        
        context['title'] = 'Eliminar servicio'
        context['text'] = 'Estas seguro que desea eliminar el servicio?'
        context['url_redirect'] = reverse_lazy('system:service_list')
        return context


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

        data = {}
        data['form_is_valid'] = False
        
        try:
            action = request.POST['action_service']
            print(request.POST)
            if action == 'pay':
                form = self.get_form()
                if form.is_valid():
                    user_card = User_Card.objects.get(
                        card_number=request.POST['card_number'])
                    service = self.object
                    if user_card.balance >= service.import_service:
                        if user_card.currency_type == 'CUP':

                            user_card.balance -= service.import_service
                            service.checked = True
                            user_card.save()
                            service.save()
                            form.save()
                            data['form_is_valid'] = True
                        else:
                            data['error'] = 'La moneda debe ser CUP'
                    else:
                        data['error'] = 'Saldo insuficiente para realizar la operación'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción'
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'El servicio ha sido pagado con éxito.'}
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        user_cards = User_Card.objects.filter(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pagar Servicio'

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

        data = {}
        data['form_is_valid'] = False

        try:
            action = request.POST['action_update']
            print(request.POST)
            if action == 'edit':
                form = self.get_form()

                if form.is_valid():
                    service_type = request.POST['service_type']
                    id = request.POST['service_id']
                    if service_type == 'electricidad':
                        service = Electricity_Service.objects.get(
                            electricity_id=id)
                        form.instance.import_service = service.electricity_cost

                    else:
                        service = Gas_Service.objects.get(gas_id=id)
                        form.instance.import_service = service.gas_cost

                    form.save()
                    data['form_is_valid'] = True

                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
                
        except Gas_Service.DoesNotExist:
            data['error'] = 'El servicio no existe!'
        except Electricity_Service.DoesNotExist:
            data['error'] = 'El servicio no existe!'
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'El servicio ha sido actualizado con éxito.'}
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            return redirect(self.success_url)

