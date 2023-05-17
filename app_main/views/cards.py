from django.views.generic import ListView
from ..models import *


class CardListView(ListView):
    model = User_Card
    template_name = 'cards.html'
