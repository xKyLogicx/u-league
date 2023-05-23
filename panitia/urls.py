from django.urls import path 
from . import views
from .views import *

app_name = 'panitia'

urlpatterns = [
        path('', views.panitia_home, name='panitia_home'),
        path('list/', views.show_homelist, name='show_homelist'),
        path('add/', views.show_addpertandingan, name='show_addpertandingan'),
        path('stadium/', views.show_liststadium, name='show_liststadium'),
        path('buat/', views.show_buatpertandingan, name='show_buatpertandingan'),
        path('mulai_pertandingan/', views.mulai_pertandingan, name='mulai_pertandingan'),
        path('mulai_pertandingan/pilih_peristiwa/', views.pilih_peristiwa, name='pilih_peristiwa'),
        path('incomplete/', show_incomplete, name='show_incomplete'),
        path('tablelist/', show_tablelist, name='show_tablelist'),
        path('listperistiwa/', show_listperistiwa, name='show_listperistiwa'),
        path('finished/', show_finished, name='show_finished'),
]