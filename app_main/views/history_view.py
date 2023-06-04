from itertools import chain
from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView
from ..models import Transfer, Service_Pay


class HistorialView(ListView):
    model = Transfer
    template_name = 'historial.html'
    context_object_name = 'historial'

    def get_queryset(self):
        user = self.request.user
        transfers = Transfer.objects.filter(user=user)
        service_pays = Service_Pay.objects.filter(user=user, checked=True)

        queryset = sorted(chain(transfers, service_pays),
                          key=lambda i: i.date, reverse=True)
        for object in queryset:
            object.model_name = ContentType.objects.get_for_model(object).model
            print(object.model_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
