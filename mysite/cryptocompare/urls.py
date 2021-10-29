from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name ='cryptocompare'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('register/', views.register, name='register'),
    path('crypto_login/', views.crypto_login, name='crypto_login'),
    path('crypto_list/', views.crypto_list, name='crypto_list'),
    path('portfolio_compare/', views.portfolio_compare, name='portfolio_compare'),
    path('delete_crypto/', views.delete_crypto, name='delete_crypto'),
    
    ]