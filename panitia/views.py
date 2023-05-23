from django.shortcuts import render

# Create your views here.
def panitia_home(request):
    return render(request, 'panitia_home.html')

def show_homelist(request):
    return render(request, "homelist.html")

def show_addpertandingan(request):
    return render(request, "addpertandingan.html")

def show_liststadium(request):
    return render(request, "liststadium.html")

def show_buatpertandingan(request):
    return render(request, "buatpertandingan.html")

def mulai_pertandingan(request):
    return render(request, "mulaipertandingan.html")

def pilih_peristiwa(request):
    return render(request, "pilihperistiwa.html")

def show_incomplete(request):
    return render(request, "incomplete.html")

def show_listperistiwa(request):
    return render(request, "listperistiwa.html")

def show_tablelist(request):
    return render(request, "tablelist.html")

def show_finished(request):
    return render(request, "finished.html")