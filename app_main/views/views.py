from ..models import User, User_Card, Person_DB, Phone_DB, Bank_DB
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.db import IntegrityError
from ..forms import *

# Create your views here.


def main_page(request):
    return render(request, 'index.html')


def error_page(request):
    return render(request, 'error_page.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {
            'form': CustomUserCreationForm
        })
    else:

        try:
            phone = Phone_DB.objects.get(number=request.POST['phone'])
            person = Person_DB.objects.get(dni=request.POST['dni'])
            if not phone.associated and not person.register:
                if request.POST['password1'] == request.POST['password2']:
                    try:
                        print(request.POST)
                        print(person.dni)
                        print(phone.number)
                        person.user_set.create(
                            ci=request.POST['dni'], user_name=request.POST['username'], password=request.POST['password1'], phone=request.POST['phone'])

                        return redirect('signin')
                    except IntegrityError:
                        return render(request, 'signup.html', {
                            'form': CustomUserCreationForm,
                            'error': 'User already exist'
                        })

                else:
                    return render(request, 'signup.html', {
                        'form': CustomUserCreationForm,
                        'error': 'Password do not match'
                    })

            else:
                return render(request, 'signup.html', {
                    'form': CustomUserCreationForm,
                    'error': 'Phone or CI not found!'
                })

        except:
            return redirect('error_page')


def signout(request):
    logout(request)
    return redirect('main')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        print(request.POST)
        if user is None:
            print('jhhjhhjh')
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'user or pass are incorrect'
            })
        else:
            login(request, user)
            return render(request, 'operations.html')


def operations(request):
    return render(request, 'operations.html')
