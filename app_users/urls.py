from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', UsersLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='signup')
]
