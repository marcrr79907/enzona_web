from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..mixins import IsSuperuserMixin

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class MainView(LoginRequiredMixin, IsSuperuserMixin, TemplateView):
    template_name = 'main.html'


class HistoryView(TemplateView):
    template_name = 'historial.html'


class TermsView(TemplateView):
    template_name = 'terms_conditions.html'


class ContactView(TemplateView):
    template_name = 'contactenos.html'
