from ..models import User_Card, Person_DB, Phone_DB, Bank_DB
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import TemplateView
from ..forms import *

# Create your views here.


def main_page(request):
    return render(request, 'index.html')


def error_page(request):
    return render(request, 'error_page.html')


def operations(request):
    return render(request, 'operations.html')


class IndexView(TemplateView):
    template_name = 'index.html'
