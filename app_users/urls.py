from django.urls import path
from .views import UsersView

app_name = 'users'

urlpatterns = [
    path('log/', UsersView.as_view(), name='login')

]
