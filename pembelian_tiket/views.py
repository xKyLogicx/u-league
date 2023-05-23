from django.shortcuts import render

# Create your views here.
def show_beli(request):
    return render(request, "belitiket.html")

def show_listpertandingan(request):
    return render(request, "listpertandingan.html")

def show_listwaktu(request):
    return render(request, "listwaktu.html")

def show_pilihstadium(request):
    return render(request, "pilihstadium.html")