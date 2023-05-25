from django.shortcuts import render
from django.contrib import messages
import psycopg2
import locale
import uuid
from utils.query import *
from django.views.decorators.csrf import csrf_exempt
from manager import views as manager_views
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

@csrf_exempt
def show_tablelist(request):
    context = {}
    
    username = request.session['username']
    
    tim1_query = query(f"""
                        SELECT t.nama_tim, p.start_datetime, tp.skor
                        FROM pertandingan p
                        JOIN tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan
                        JOIN tim t ON tp.nama_tim = t.nama_tim
                        LEFT JOIN tim_manajer tm ON t.nama_tim = tm.nama_tim
                        LEFT JOIN rapat r ON tm.id_manajer = r.manajer_tim_a
                        LEFT JOIN panitia pa ON r.perwakilan_panitia = pa.id_panitia
                        WHERE pa.username = '{username}'
                        GROUP BY 1, 2, 3""")
    
    tim2_query = query(f"""
                        SELECT t.nama_tim, p.start_datetime , tp.skor
                        FROM pertandingan p
                        JOIN tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan
                        JOIN tim t ON tp.nama_tim = t.nama_tim
                        LEFT JOIN tim_manajer tm ON t.nama_tim = tm.nama_tim
                        LEFT JOIN rapat r ON tm.id_manajer = r.manajer_tim_b
                        LEFT JOIN panitia pa ON r.perwakilan_panitia = pa.id_panitia
                        WHERE pa.username = '{username}'
                        GROUP BY 1, 2, 3""")
    
    nama_tim1 = tim1_query[0]['nama_tim']
    nama_tim2 = tim2_query[0]['nama_tim']
    
    skor_tim1 = tim1_query[0]['skor']
    skor_tim2 = tim2_query[0]['skor']
    
    pemenang_query = query(f"""
                           SELECT 
                           CASE 
                           WHEN CAST('{skor_tim1}' AS INTEGER) > CAST('{skor_tim2}' AS INTEGER) THEN '{nama_tim1}'
                           WHEN CAST('{skor_tim1}' AS INTEGER) < CAST('{skor_tim2}' AS INTEGER) THEN '{nama_tim2}'
                           END AS pemenang
                           FROM tim_pertandingan tp
                           JOIN pertandingan p ON tp.id_pertandingan = p.id_pertandingan
                           JOIN rapat r ON p.id_pertandingan = r.id_pertandingan
                           JOIN panitia pa ON r.perwakilan_panitia = pa.id_panitia
                           WHERE pa.username = '{username}'
                           GROUP BY 1""")
    
                               
    time_pertandingan = query(f"""
                                    SELECT p.start_datetime
                                    FROM pertandingan p
                                    JOIN tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan
                                    JOIN tim t ON tp.nama_tim = t.nama_tim
                                    LEFT JOIN tim_manajer tm ON t.nama_tim = tm.nama_tim
                                    LEFT JOIN rapat r ON p.id_pertandingan = r.id_pertandingan
                                    LEFT JOIN panitia pa ON r.perwakilan_panitia = pa.id_panitia
                                    WHERE pa.username = '{username}'
                                    GROUP BY 1""")
                                    
    
    context = {
        'tim1' : tim1_query,
        'tim2' : tim2_query,
        'pemenang' : pemenang_query,
        'waktu' : time_pertandingan
    }
    
    return render(request, "tablelist.html", context=context)

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
 
@csrf_exempt
def manage_pertandingan(request):
    username = request.session['username']
    
    list_pertandingan = query(f"""
                              SELECT * from pertandingan
                              JOIN peristiwa ON pertandingan.id_pertandingan = peristiwa.id_pertandingan
                              JOIN wasit_bertugas ON pertandingan.id_pertandingan = wasit_bertugas.id_pertandingan
                              JOIN tim_pertandingan ON pertandingan.id_pertandingan = tim_pertandingan.id_pertandingan
                              LEFT JOIN rapat ON pertandingan.id_pertandingan = rapat.id_pertandingan
                              WHERE perwakilan_panitia = '{username}'
                              GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9""")
    
    print ("try")
    print (list_pertandingan)
    print (list_pertandingan[0]['id_pertandingan'])
    
    if list_pertandingan[0]['id_pertandingan'] == None:
        print ("belum ada pertandingan")
        print (list_pertandingan[0]['id_pertandingan'])
        return HttpResponseRedirect(reverse('panitia:show_incomplete'))
    
    return HttpResponseRedirect(reverse('panitia:show_tablelist'))