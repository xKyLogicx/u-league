from django.urls import path
from pembelian_tiket.views import show_beli, show_listpertandingan, show_listwaktu, show_pilihstadium

app_name = 'pembelian_tiket'

urlpatterns = [
    path('', show_pilihstadium, name='show_pilihstadium'),
    path('waktu', show_listwaktu, name='show_listwaktu'),
    path('pertandingan', show_listpertandingan, name='show_listpertandingan'),
    path('beli', show_beli, name='show_beli'),
]