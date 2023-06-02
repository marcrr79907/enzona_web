from django.urls import path
from .views import views, cards_view, transfer_view, service_view

app_name = 'system'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),

    path('historial/', views.HistoryView.as_view(), name='historial'),
    path('terms_conditions/', views.TermsView.as_view(), name='terms_conditions'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('main/', views.MainView.as_view(), name='main'),
    # Tarjetas
    path('card_list/', cards_view.CardListView.as_view(), name='card_list'),
    path('card_create/',
         cards_view.CardCreateView.as_view(), name='card_create'),
    path('card_delete/<int:pk>',
         cards_view.CardDeleteView.as_view(), name='card_delete'),
    # Transferencias
    path('transfer_create/',
         transfer_view.TranferCreateView.as_view(), name='transfer_create'),
    path('transfer_list/',
         transfer_view.TranferCreateView.as_view(), name='transfer_list'),
    # Servicios
    path('service_list/', service_view.ServiceListView.as_view(),
         name='service_list'),
    path('service_create/', service_view.ServiceCreateView.as_view(),
         name='service_create'),
    path('service_update/<int:pk>', service_view.ServiceUpdateView.as_view(),
         name='service_update'),
    path('service_pay/<int:pk>', service_view.ServicePayView.as_view(),
         name='service_pay'),
    path('service_delete/<int:pk>', service_view.ServiceDeleteView.as_view(),
         name='service_delete')
]
