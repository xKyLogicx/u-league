from django.urls import path 
from . import views
from .views import *

app_name = 'penonton'

urlpatterns = [
        path('', views.penonton_home, name='penonton_home'),
        path('listpertandingan/', views.show_listpertandingan, name='listpertandingan'),
        path('pilihstadium/', show_pilihstadium, name='show_pilihstadium'),
        path('waktu/', show_listwaktu, name='show_listwaktu'),
        path('pertandingan/', show_listpertandingan, name='show_listpertandingan'),
        path('beli/', show_beli, name='show_beli'),
]
