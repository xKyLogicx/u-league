from django.shortcuts import render
from utils.query import *

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def penonton_home(request):
    return render(request, 'penonton_home.html')

def show_listpertandingan_penonton(request):
    query_listpertandingan = query(f"""
    SELECT
        tp1.Nama_Tim AS Nama_Tim_A,
        tp2.Nama_Tim AS Nama_Tim_B,
        s.Nama AS Stadium,
        p.Start_Datetime
    FROM Pertandingan AS p
    LEFT JOIN Stadium AS s ON p.Stadium = s.ID_Stadium
    LEFT JOIN Tim_Pertandingan AS tp1 ON p.ID_Pertandingan = tp1.ID_Pertandingan
    LEFT JOIN Tim_Pertandingan AS tp2 ON p.ID_Pertandingan = tp2.ID_Pertandingan
    ORDER BY p.Start_Datetime ASC;
    """)

    print(query_listpertandingan)
    context={
        'listpertandingan':query_listpertandingan
    }

    return render(request, "listpertandingan_penonton.html", context=context)

def show_beli(request):
    query_pembelian = query(f"""
    
    """)

    print(query_pembelian)

    context={
        'pembelian':query_pembelian
    }


    #variable query untuk setiap pembelian
    #POST & GET untuk setiap tombol beli
    #Siapin if ketika yang querynya tidak sesuai diharapin keluarin
    #notif kalau itu salah.
    #jika berhasil maka arahin ke dashboard

    return render(request, "belitiket.html", context=context)

def listpertandinganbeli(request):
    
    #pengambilan data
    selected_time = request.session.get('selected_time')
    selected_stadium = request.session.get('selected_stadium')
    selected_date = request.session.get('selected_date')

    query_listpertandinganbeli = query(f"""
    SELECT
        tp1.Nama_Tim AS Nama_Tim_A,
        tp2.Nama_Tim AS Nama_Tim_B,
        s.Nama AS Stadium,
        p.Start_Datetime
    FROM Pertandingan AS p
    LEFT JOIN Stadium AS s ON p.Stadium = s.ID_Stadium
    LEFT JOIN Tim_Pertandingan AS tp1 ON p.ID_Pertandingan = tp1.ID_Pertandingan
    LEFT JOIN Tim_Pertandingan AS tp2 ON p.ID_Pertandingan = tp2.ID_Pertandingan
    WHERE s.Nama = '{selected_stadium}'
    AND p.Start_Datetime >= '{selected_date} {selected_time}'
    ORDER BY p.Start_Datetime ASC;
    """)

    print(query_listpertandinganbeli)

    context={
        'listpertandinganbeli':query_listpertandinganbeli,
        'selected_time':selected_time,
        'selected_stadium':selected_stadium,
        'selected_date':selected_date
    }

    if request.method == 'POST':
        selected_pertandingan = request.POST.get('pertandingan')
        request.session['selected_pertandingan'] = selected_pertandingan
        print(selected_pertandingan)

        return HttpResponseRedirect(reverse('penonton:show_beli'))

    return render(request, "listpertandinganbeli.html", context=context)

def show_listwaktu(request):
    
    # NGAMBIL DATA
    selected_stadium = request.session.get('selected_stadium')
    selected_date = request.session.get('selected_date')

    print(selected_stadium)
    print(selected_date)
    
    # NGAMBIL QUERY
    query_listwaktu = query(f"""
    SELECT DISTINCT Start_Datetime, End_Datetime
    FROM Pertandingan, Stadium
    WHERE Stadium.Nama = '{selected_stadium}'
    AND Start_Datetime >= '{selected_date}'
    """)

    split_time = []

    for item in query_listwaktu:
        start_time = item['start_datetime'].strftime('%H:%M')
        end_time = item['end_datetime'].strftime('%H:%M')
        split_time.append({'start_time': start_time, 'end_time': end_time})

    print(split_time)
    print(query_listwaktu)

    context={
        'selected_stadium':selected_stadium,
        'list_waktu':query_listwaktu,
        'split_time':split_time
    }

    if request.method == 'POST':
        selected_time = request.POST.get('time')
        request.session['selected_time'] = selected_time
        print(selected_time)

        return HttpResponseRedirect(reverse('penonton:listpertandinganbeli'))

    return render(request, "listwaktu.html", context=context)

def show_pilihstadium(request):

    # NGAMBIL QUERY STADIUM
    query_liststadium = query(f"""
    SELECT * FROM STADIUM
    """)

    context={
        'nama_stadium':query_liststadium
    }

    # GET DATA INPUT USERS
    if request.method == 'POST':
        selected_stadium = request.POST.get('stadium')
        selected_date = request.POST.get('tanggal')

        request.session['selected_stadium'] = selected_stadium
        request.session['selected_date'] = selected_date

        print(selected_date)
        print(selected_stadium)
        
        return HttpResponseRedirect(reverse('penonton:show_listwaktu'))
    
    return render(request, "pilihstadium.html", context=context)