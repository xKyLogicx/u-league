from django.shortcuts import render
from utils.query import *


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
    query_listpertandingan = query(f"""
    
    """)

    print(query_listpertandingan)

    context={
        'listpertandingan':query_listpertandingan
    }

    #variable query untuk setiap tim
    #potong bagi dua yang tim 1 & tim 2
    #context query untuk tim 1 & tim 2
    #POST & GET untuk dapetin values --> biar bisa di beli

    return render(request, "listpertandinganbeli.html", context=context)

def show_listwaktu(request):
    
    #kalo bisa dapetin jam yang ada pada stadium tersebut
    query_listwaktu = query(f"""
    
    """)

    print(query_listwaktu)

    context={
        'list_waktu':query_listwaktu
    }

    selected_stadium = request.session.get('selected_stadium')
    selected_date = request.session.get('selected_date')

    print(selected_stadium)
    print(selected_date)

    #asumsi yang kita dapet ('2023-01-02 13:00:00', '2023-01-04 15:00:00'),

    time_list = []

    for start_time, end_time in selected_date:
        start_hour = start_time.split(' ')[1].split(':')[0]
        start_minute = start_time.split(' ')[1].split(':')[1]
        end_hour = end_time.split(' ')[1].split(':')[0]
        end_minute = end_time.split(' ')[1].split(':')[1]
        time_list.append((start_hour, end_hour))

    #maka outputnya [    ('13', '15'),    ('14', '16'), ...

    #bingung cara biar bisa diambil dan di taro ke HTMLnya





    print(time_list)
    #variable query untuk list waktu
    #potong pake list atau apapun itu biar sisa jamnya aja diambil
    #POST & GET untuk dapetin values --> biar bisa di next

    return render(request, "listwaktu.html", context=context)

def show_pilihstadium(request):
    query_liststadium = query(f"""
    SELECT * FROM STADIUM
    """)

    context={
        'nama_stadium':query_liststadium
    }

    if request.method == 'POST':
        selected_stadium = request.POST.get('stadium')
        selected_date = request.POST.get('tanggal')
        # Process the selected stadium and date as needed
        
        # Redirect to the next page (show_listwaktu) passing the selected stadium and date
        return redirect(reverse('penonton:show_listwaktu'))

    return render(request, "pilihstadium.html", context=context)