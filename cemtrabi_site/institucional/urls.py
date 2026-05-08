from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('medicina-ocupacional/', views.medicina, name='medicina'),
    path('seguranca-do-trabalho/', views.seguranca, name='seguranca'),
    path('treinamentos/', views.treinamentos, name='treinamentos'),
    path('contato/', views.contato, name='contato'),
    path('encaminhamento/', views.encaminhamento, name='encaminhamento'),
    path('politica-privacidade/', views.politica_privacidade, name='politica_privacidade'),
    path('sobre-nos/', views.sobre, name='sobre'),
]
