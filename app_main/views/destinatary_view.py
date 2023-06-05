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
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    number=int(request.POST['associated_card'])
                    card = Bank_DB.objects.get(
                        card_number=number)
                    form.instance.user = self.request.user

                    destinatary_list = Destinatary.objects.filter(user=self.request.user)
                    for destinatary_card in destinatary_list:
                        if destinatary_card.associated_card == card.card_number:

                            data['error'] = 'Ya existe un destinatario con esta tarjeta asociada'
                            return redirect('system:destinatary_list', {
                                'data': data
                            })
                       
                    data = form.save()
                    print(action)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        except Exception as e:
            data['error'] = str(e)

        return redirect('system:destinatary_list')
    

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


class DestinataryUpdateView(LoginRequiredMixin, DeleteView):
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
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    card = Bank_DB.objects.get(
                        card_number=request.POST['card_number'])
                    

                    destinatary_list = Destinatary.objects.filter(user=self.request.user)
                    for destinatary_card in destinatary_list.associated_card:
                        if destinatary_card == card.card_number:
                            data['error'] = 'Ya existe un destinatario con esta tarjeta asociada'
                            return redirect('system:destinatary_list', {
                                'data': data
                            })
                       
                    data = form.save()
                else:
                    data['error'] = form.errors    
                
            else:
                data['error'] = 'No ha ingresado ninguna acción'
        except Exception as e:
            data['error'] = str(e)

        print(data)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar destinatario'
        context['action'] = 'edit'

        return context 

