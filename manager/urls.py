from django.urls import path 
from . import views
from .views import *

app_name = 'manager'

urlpatterns = [
        path('', views.manager_home, name='manager_home'),
        path('mengelola_tim/', views.mengelola_tim, name='mengelola_tim'),
        path('registrasi/', views.show_timregist, name='show_timregist'),
        path('detail/', views.show_teamdetail, name='show_teamdetail'),
        path('pemain/', views.show_addpemain, name='show_addpemain'),
        path('pelatih/', views.show_addpelatih, name='show_addpelatih'),
        path('update_captain/', views.make_captain, name='make_captain'),
        path('delete_pemain/', views.delete_pemain, name='delete_pemain'),
        path('delete_pelatih/', views.delete_pelatih, name='delete_pelatih'),
        path('add_coach/', views.add_coach, name='add_coach'),
        path('add_player/', views.add_player, name='add_player'),
        path('historyrapat/', views.show_historyrapat, name='history_rapat'),
        path('listpertandingan/', views.show_listpertandingan, name='listpertandingan'),
        path('listpemesanan/', show_listpemesanan, name='show_listpemesanan'),
        path('ketersediaanstadium/', show_ketersediaanstadium, name='show_ketersediaanstadium'),
        path('stadium/', show_memesanstadium, name='show_memesanstadium'),

]
