
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from ..mixins import IsSuperuserMixin
from ..models import *
from ..forms import *


class TranferCreateView(LoginRequiredMixin, IsSuperuserMixin, CreateView):
    model = Transfer
    form_class = TranferForm
    template_name = 'transfers/trnsfer_create.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user_id = self.request.user

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        data = {}
        print(self.get_object)
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    card = Bank_DB.objects.get(
                        card_number=request.POST['card_number'])
                    if not card.associated:
                        if request.POST['pin'] == card.pin:
                            data = form.save()
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
