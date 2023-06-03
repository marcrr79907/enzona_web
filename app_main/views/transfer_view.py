
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from ..models import *
from ..forms import *


class TranferCreateView(LoginRequiredMixin, CreateView):
    model = Transfer
    form_class = TransferForm
    template_name = 'transferencia/transferencias.html'
    success_url = reverse_lazy('system:transfer_list')

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
                    origin = request.POST['origin_card']
                    dest = request.POST['dest_card']
                    transfer_import = request.POST['import_transfer']

                    user_org = User_Card.objects.get(card_number=origin)
                    origin_card = Bank_DB.objects.get(card_number=origin)
                    dest_card = Bank_DB.objects.get(card_number=dest)
                    
                    mont = int(transfer_import)
                    if origin != dest and origin_card.currency_type == dest_card.currency_type:
                        if mont > 0:
                            if user_org.balance >= mont:
                                form.instance.user = self.request.user
                                if dest_card.associated:
                                    user_dest = User_Card.objects.get(card_number=dest)
                                    user_dest.balance += mont
                                    user_dest.save()

                                dest_card.balance += mont
                                user_org.balance -= mont
                                origin_card.balance -= mont
                                
                                dest_card.save()
                                user_org.save()
                                
                                data = form.save()

                            else:
                                data['error'] = 'Saldo insuficiente'
                        else:
                            data['error'] = 'El saldo a transferir no puede ser cero'
                    else:
                        data['error'] = 'Las tarjetas no pueden ser iguales'
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        except Exception as e:
            data['error'] = str(e)

        return redirect('system:transfer_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Transferencia'
        context['card_list'] = User_Card.objects.filter(user=self.request.user)
        context['action'] = 'add'
        context['list_url'] = 'system:transfer_create'

        return context


class TranferListView(LoginRequiredMixin, ListView):
    model = Transfer
    template_name = 'transferencia/transferencias.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        transfers = Transfer.objects.filter(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de transferencias'
        context['list_url'] = reverse_lazy('system:transfer_create')
        context['entity'] = Transfer
        context['object_list'] = transfers
        context['card_list'] = User_Card.objects.filter(user=self.request.user)
        context['action'] = 'add'

        return context
