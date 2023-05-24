from django.urls import path 
from . import views
from .views import *

app_name = 'penonton'

urlpatterns = [
        path('', views.penonton_home, name='penonton_home'),
        path('listpertandingan/', views.listpertandinganbeli, name='listpertandinganbeli'),
        path('pilihstadium/', show_pilihstadium, name='show_pilihstadium'),
        path('waktu/', show_listwaktu, name='show_listwaktu'),
        path('pertandingan/', views.show_listpertandingan_penonton, name='show_listpertandingan_penonton'),
        path('beli/', show_beli, name='show_beli'),
]
