from django.urls import path
from r_listpertandingan.views import show_listpertandingan
from . import views

app_name = 'r_listpertandingan'

urlpatterns = [
    path('listpertandingan/', views.show_listpertandingan, name='show_listpertandingan'),
]