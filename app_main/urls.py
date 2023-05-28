from django.urls import path
from .views import views, cards_view


urlpatterns = [
    path('', views.main_page, name='main'),
    path('signup/', views.signup, name='signup'),
    path('operations/', views.operations, name='operations'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('error/', views.error_page, name='error_page'),
    path('card_create/', cards_view.CardCreateView.as_view(), name='card_create')
]
