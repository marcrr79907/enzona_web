from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from ..models import *
from ..forms import *



class DestinataryListView(LoginRequiredMixin, ListView):
    model = Destinatary
    template_name = 'destinatary/destinary.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        destinatary_list = Destinatary.objects.filter(
            user=self.request.user)

        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Mis Destinatarios'
        context['title'] = 'Agregar Destinatario'
        context['entity'] = Destinatary
        context['object_list'] = destinatary_list
        context['data'] = self.request.session.pop('data', None)
        context['action_update'] = 'edit'
        context['action'] = 'add'

        return context
    

class DestinataryCreateView(LoginRequiredMixin, CreateView):
    model = Destinatary
    form_class = DestinataryForm
    template_name = 'destinatary/destinary.html'
    success_url = reverse_lazy('system:destinatary_list')

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
                    number=int(request.POST['associated_card'])
                    name=request.POST['name']
                    card = Bank_DB.objects.get(
                        card_number=number)
                    form.instance.user = self.request.user

                    destinatary_list = Destinatary.objects.filter(user=self.request.user)
                    for destinatary in destinatary_list:
                        if destinatary.associated_card == number:

                            request.session['data'] = {
                            'error_message': 'Ya existe un destinatario con esta tarjeta asociada!'}
                            return redirect(self.success_url)
                        elif destinatary.name == name:

                            request.session['data'] = {
                            'error_message': 'Ya existe un destinatario con este nombre!'}
                            return redirect(self.success_url)

                    form.save()
                    data['form_is_valid'] = True
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'

        except Bank_DB.DoesNotExist:
            data['error'] = 'La tarjeta no existe!'
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'El destinatario ha sido creado con éxito.'}
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            return redirect(self.success_url)
    

class DestinataryDeleteView(LoginRequiredMixin, DeleteView):
    model = Destinatary
    success_url = reverse_lazy('system:destinatary_list')
    template_name = 'eliminar.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar destinatario'
        context['text'] = 'Está seguto de eliminar el destinatario?'
        context['url_redirect'] = reverse_lazy('system:destinatary_list')

        return context


class DestinataryUpdateView(LoginRequiredMixin, UpdateView):
    model = Destinatary
    form_class = DestinataryForm
    template_name = 'destinatary/destinary.html'
    success_url = reverse_lazy('system:destinatary_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        data['form_is_valid'] = False

        try:
            action = request.POST['action_update']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    number=int(request.POST['associated_card'])
                    name=request.POST['name']
                    card = Bank_DB.objects.get(card_number=number)

                    destinatary_list = Destinatary.objects.filter(user=self.request.user)
                    for destinatary in destinatary_list:

                        if self.object.associated_card == number or self.object.name == name:
                            pass
                        elif destinatary.associated_card == number:

                            request.session['data'] = {
                            'error_message': 'Ya existe un destinatario con esta tarjeta asociada!'}
                            return redirect(self.success_url)
                        elif destinatary.name == name:

                            request.session['data'] = {
                            'error_message': 'Ya existe un destinatario con este nombre!'}
                            return redirect(self.success_url)
                       
                    form.save()
                    data['form_is_valid'] = True

                else:
                    data['error'] = form.errors    
                
            else:
                data['error'] = 'No ha ingresado ninguna acción'
        except Bank_DB.DoesNotExist:
            data['error'] = 'La tarjeta no existe!'
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'El destinatario ha sido actualizado con éxito.'}
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar destinatario'

        return context 

