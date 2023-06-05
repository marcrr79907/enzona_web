from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from ..models import *
from ..forms import *


class CardListView(LoginRequiredMixin, ListView):
    model = User_Card
    template_name = 'card/credit_card.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cards_list = User_Card.objects.filter(
            user=self.request.user)

        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Mis Tarjetas'
        context['title'] = 'Agregar Tarjeta'
        context['entity'] = User_Card
        context['object_list'] = cards_list
        context['action'] = 'add'
        context['data'] = self.request.session.pop('data', None)

        return context


class CardCreateView(LoginRequiredMixin, CreateView):
    model = User_Card
    form_class = CardForm
    template_name = 'card/credit_card.html'
    success_url = reverse_lazy('system:card_list')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        data['form_is_valid'] = False
        try:
            action = request.POST['action']
            print(action)
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    card = Bank_DB.objects.get(
                        card_number=request.POST['card_number'])
                    if not card.associated:
                        if request.POST['pin'] == card.pin:
                            form.instance.user = self.request.user
                            form.instance.bank_type = card.bank_type
                            form.instance.currency_type = card.currency_type
                            form.instance.balance = card.balance
                            card.associated = True

                            card.save()
                            form.save()
                            data['form_is_valid'] = True
                        else:
                            data['form_is_valid'] = False
                            data['error'] = 'Pin incorrecto'
                    else:
                        data['form_is_valid'] = False
                        data['error'] = 'La tarjeta ya está asociada a un usuario!'
                else:
                    data['form_is_valid'] = False
                    data['error'] = form.errors
            else:
                data['form_is_valid'] = False
                data['error'] = 'No ha ingresado ninguna acción!'
        
        except Bank_DB.DoesNotExist:
            data['error'] = 'La tarjeta de no existe'
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'La tarjeta ha sido creada con éxito.'}
            print(request.session['data'])
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            print(request.session['data'])
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'User_Card'
        context['list_url'] = reverse_lazy('card_create')

        return context


class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = User_Card
    success_url = reverse_lazy('system:card_list')
    url_redirect = success_url
    template_name = 'eliminar.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:

            user_card = User_Card.objects.get(id=self.object.id)
            bank_card = Bank_DB.objects.get(card_number=user_card.card_number)

            bank_card.associated = False
            bank_card.save()
        except:
            pass
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        
        context['title'] = 'Eliminar tarjeta'
        context['text'] = 'Estas seguro que desea eliminar la tarjta?'
        context['url_redirect'] = reverse_lazy('system:card_list')
        return context
   
    
