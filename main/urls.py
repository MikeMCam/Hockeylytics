from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('stats/', views.my_stats, name='my_stats'),
    path('clients/', views.clients, name='clients'),
]
