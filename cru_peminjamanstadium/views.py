from django.shortcuts import render

# Create your views here.
def show_listpemesanan(request):
    return render(request, "listpemesan.html")

def show_ketersediaanstadium(request):
    return render(request, "ketersediaanstadium.html")

def show_memesanstadium(request):
    return render(request, "memesanstadium.html")