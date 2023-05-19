from django.urls import path
from .views import views, cards_view


urlpatterns = [
    path('', views.main_page, name='main'),
    path('signup/', views.signup, name='signup'),
    path('operations/', views.operations, name='operations'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('error/', views.error_page, name='error_page'),
    path('card_list/', cards_view.CardListView.as_view(), name='card_list'),
    path('card_create/', cards_view.CardCreateView.as_view(), name='card_create'),
    path('card_edit/<int:pk>/',
         cards_view.CardUpdateView.as_view(), name='card_update'),
    path('card_delete/<int:pk>/',
         cards_view.CardDeleteView.as_view(), name='card_delete')
]
