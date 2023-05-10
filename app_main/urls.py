from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),
    path('singup/', views.singup, name='singup'),
    path('operations/', views.operations, name='operations')
]
