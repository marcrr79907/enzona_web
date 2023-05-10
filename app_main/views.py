from .models import User, User_Card, Bank_DB, Person_DB, Phone_DB
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse

# Create your views here.


def main_page(request):
    return render(request, 'index.html')


def singup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('operations')
            except:
                return HttpResponse('Username already exists')

        return HttpResponse('Password do not match')


def operations(request):
    return render(request, 'operations.html')
