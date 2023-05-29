from django.urls import path
from .views import views, cards_view, transfer_view

app_name = 'system'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('main/', views.MainView.as_view(), name='main'),
    # Tarjetas
    path('card_list/', cards_view.CardListView.as_view(), name='card_list'),
    path('card_create/',
         cards_view.CardCreateView.as_view(), name='card_create'),
    path('card_edit/<int:pk>/',
         cards_view.CardUpdateView.as_view(), name='card_update'),
    path('card_delete/<int:pk>/',
         cards_view.CardDeleteView.as_view(), name='card_delete'),
    path('card_form/',
         cards_view.CardFormView.as_view(), name='card_form'),
    # Transferencias
    path('transfer_create/',
         transfer_view.TranferCreateView.as_view(), name='transfer_create')
]
