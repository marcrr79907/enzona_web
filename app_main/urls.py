from django.urls import path
from .views import views, cards_view, transfer_view, service_view, destinatary_view, destinatary_view, history_view

app_name = 'system'

urlpatterns = [
     # Pagina de inicio
     path('', views.IndexView.as_view(), name='home'),
     # historial
     path('history/', history_view.HistorialView.as_view(), name='history'),
     
     path('terms_conditions/', views.TermsView.as_view(), name='terms_conditions'),
     path('contact/', views.ContactView.as_view(), name='contact'),
     path('main/', views.MainView.as_view(), name='main'),
     # Servicios
     path('service_list/', service_view.ServiceListView.as_view(), name='service_list'),
     path('service_create/', service_view.ServiceCreateView.as_view(), name='service_create'),
     path('service_update/<int:pk>', service_view.ServiceUpdateView.as_view(), name='service_update'),
     path('service_delete/<int:pk>', service_view.ServiceDeleteView.as_view(), name='service_delete'),
     path('service_pay/<int:pk>', service_view.ServicePayView.as_view(), name='service_pay'),
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
          transfer_view.TranferListView.as_view(), name='transfer_list'),
     # Destinatarios
     path('destinatary_list/',
          destinatary_view.DestinataryListView.as_view(), name='destinatary_list'),
     path('destinatary_delete/<int:pk>',
          destinatary_view.DestinataryDeleteView.as_view(), name='destinatary_delete'),
     path('destinatary_create/',
          destinatary_view.DestinataryCreateView.as_view(), name='destinatary_create'),
     path('destinatary_update/<int:pk>',
          destinatary_view.DestinataryUpdateView.as_view(), name='destinatary_update')                    

]
