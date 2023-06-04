from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', UsersLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('editprofile/<int:pk>/', UserUpdateView.as_view(), name='editprofile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('segurity/', SegurityUserView.as_view(), name='segurity')
]
