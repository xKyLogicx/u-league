from django.shortcuts import render

# Create your views here.
def penonton_home(request):
    return render(request, 'penonton_home.html')

def show_listpertandingan(request):
    return render(request, "listpertandingan.html")

def show_beli(request):
    return render(request, "belitiket.html")

def show_listpertandingan(request):
    return render(request, "listpertandingan.html")

def show_listwaktu(request):
    return render(request, "listwaktu.html")

def show_pilihstadium(request):
    return render(request, "pilihstadium.html")