from django.shortcuts import render
from django.contrib import messages
import psycopg2
import locale
import uuid
from utils.query import *
from django.views.decorators.csrf import csrf_exempt

locale.setlocale(locale.LC_ALL, '')
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

@csrf_exempt
def panitia_home(request):
    context = {}
    username = request.session['username']
    
    panitia = query(f"""
                    SELECT np.nama_depan, np.nama_belakang, np.nomor_hp, np.email, np.alamat, string_agg(DISTINCT nps.status, ', ') as status, p.jabatan, r.datetime
                    FROM panitia p
                    JOIN non_pemain np ON p.id_panitia = np.id
                    LEFT JOIN status_non_pemain nps ON np.id = nps.id_non_pemain
                    LEFT JOIN rapat r ON p.id_panitia = r.perwakilan_panitia
                    WHERE p.username = '{username}'
                    GROUP BY 1, 2, 3, 4, 5, 7, 8""")
    context = {
        'data_panitia' : panitia
    }
    return render(request, 'panitia_home.html', context=context)

def show_homelist(request):
    return render(request, "homelist.html")

def show_addpertandingan(request):
    return render(request, "addpertandingan.html")

def show_liststadium(request):
    return render(request, "liststadium.html")

def show_buatpertandingan(request):
    return render(request, "buatpertandingan.html")

# untuk rapat
def show_rapat(request, id_pertandingan):
    if request.method == 'GET':

            pertandingan = query("""SELECT r.id_pertandingan, string_agg(nama_tim, ' vs ') as tim_bertanding, s.nama, datetime
                                FROM rapat r, pertandingan p, tim_pertandingan tp, stadium s 
                                WHERE r.id_pertandingan = p.id_pertandingan AND p.id_pertandingan = tp.id_pertandingan AND p.stadium = s.id_stadium AND r.id_pertandingan = '{}'
                                GROUP BY r.id_pertandingan, stadium, s.nama, datetime;""".format(id_pertandingan))
                
            print(pertandingan)
            context = {'pertandingan': pertandingan}

            return render(request, 'rapat.html', context)    
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

def show_pertandingan(request):
    if request.method == 'GET':

            pertandingan = query("""SELECT r.id_pertandingan, string_agg(nama_tim, ' vs ') as tim_bertanding, s.nama, datetime
                                FROM rapat r, pertandingan p, tim_pertandingan tp, stadium s 
                                WHERE r.id_pertandingan = p.id_pertandingan AND p.id_pertandingan = tp.id_pertandingan AND p.stadium = s.id_stadium 
                                GROUP BY r.id_pertandingan, stadium, s.nama, datetime;""")
                
            print(pertandingan)
            context = {'pertandingan': pertandingan}

            return render(request, 'pilihpertandingan.html', context)