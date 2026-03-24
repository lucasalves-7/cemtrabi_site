from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('medicina-ocupacional/', views.medicina, name='medicina'),
    path('seguranca-do-trabalho/', views.seguranca, name='seguranca'),
    path('treinamentos/', views.treinamentos, name='treinamentos'),
    path('contato/', views.contato, name='contato'),
    path('sobre-nos/', views.sobre, name='sobre'),
]