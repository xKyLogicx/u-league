from django.shortcuts import render
from django.contrib import messages
import psycopg2
import locale
import uuid
from utils.query import *
from django.views.decorators.csrf import csrf_exempt

locale.setlocale(locale.LC_ALL, '')

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

def manager_home(request):
    return render(request, 'manager_home.html')

@csrf_exempt
def mengelola_tim(request):
    username = "amartusewicz2"

    team = query(f"""
    SELECT * FROM Manajer
    NATURAL LEFT JOIN Tim_Manajer
    WHERE Username = '{username}'
    """)

    print("HEY COBA DULU")
    print(team)
    print(team[0]['nama_tim'])

    if team[0]['nama_tim'] is None:
        print("MASUK SINI JUGA PLS")
        print(team[0]['nama_tim'])
        return HttpResponseRedirect(reverse('manager:show_timregist'))
    
    return HttpResponseRedirect(reverse('manager:show_teamdetail'))

@csrf_exempt
def show_timregist(request):
    username = "amartusewicz2"
    if request.method == 'POST':
        team_name = request.POST.get("team_name")
        uni_name = request.POST.get("uni_name")
    
        query_add = query(f"""
        INSERT INTO TIM values ('{team_name}', '{uni_name}')""")
        
        print("\nINI HASILNYA WOI")
        print(query_add)
        print(type(query_add))

        if isinstance(query_add, psycopg2.errors.UniqueViolation):
            # msg = extract_string_before_word(str(query_add), "DETAIL")
            messages.error(request, "Nama tim tidak tersedia")
            print('ERROR NIH')
            return render(request, "teamregist.html")
        
        get_id_manajer = query(f"""
            SELECT ID_Manajer FROM MANAJER 
            WHERE Username = '{username}'""")[0]['id_manajer']
        
        query(f"""INSERT INTO Tim_Manajer values ('{get_id_manajer}', '{team_name}')""")

        return HttpResponseRedirect(reverse('manager:show_teamdetail'))
    
    return render(request, "teamregist.html")

@csrf_exempt
def show_teamdetail(request):
    context = {}

    username = "amartusewicz2"

    nama_tim = get_team(username)

    query_get_pemain = query(f"""
    SELECT Pm.ID_Pemain, CONCAT(Pm.Nama_Depan, ' ', Pm.Nama_Belakang) as Nama_Pemain, Nomor_HP, Tgl_Lahir, Is_Captain, Posisi, NPM, Jenjang 
    FROM PEMAIN Pm WHERE Pm.Nama_Tim = '{nama_tim}'
    """)

    query_get_pelatih = query(f"""
    SELECT Pl.ID_Pelatih, CONCAT(Nama_Depan, ' ', Nama_Belakang) as Nama_Pelatih, 
        Nomor_HP, Email, Alamat, string_agg(Spesialisasi, ', ') as Jenis_Spesialisasi
    FROM Non_Pemain Np, Pelatih Pl, Spesialisasi_Pelatih Sp 
    WHERE Np.ID = Pl.ID_Pelatih
    and Pl.ID_Pelatih = Sp.ID_Pelatih
    and Pl.Nama_Tim = '{nama_tim}'
    group by 1, 2, 3, 4, 5
    """)

    print("halo")
    context = {
        'pemain_list' : query_get_pemain,
        'pelatih_list' : query_get_pelatih
    }

    return render(request, "teamdetail.html", context=context)

@csrf_exempt
def show_addpemain(request):
    context = {}
    
    pemain_tersedia_list = query(f"""
        SELECT ID_Pemain, CONCAT(Nama_Depan, ' ', Nama_Belakang) as Nama_Pemain, Posisi
        FROM Pemain
        WHERE Nama_Tim is NULL
        ORDER BY Nama_Pemain ASC;
        """)

    context = {
        'pemain_tersedia_list' : pemain_tersedia_list
        }

    return render(request, "addpemain.html", context=context)

@csrf_exempt
def show_addpelatih(request):
    context = {}

    pelatih_tersedia_list = query( f"""
            SELECT Pl.ID_Pelatih, CONCAT(Nama_Depan, ' ', Nama_Belakang) as Nama_Pelatih, string_agg(Spesialisasi, ', ') as Jenis_Spesialisasi
            FROM Non_Pemain Np, Pelatih Pl, Spesialisasi_Pelatih Sp
            WHERE Np.ID = Pl.ID_Pelatih
            and Pl.ID_Pelatih = Sp.ID_Pelatih
            and Pl.Nama_Tim is NULL
            group by 1, 2
            ORDER BY Nama_Pelatih ASC;;
            """)

    context = {
        'pelatih_tersedia_list' : pelatih_tersedia_list
        }
    
    return render(request, "addpelatih.html", context=context)

@csrf_exempt
def add_player(request):
    context = {}
    username = "amartusewicz2"
    nama_tim = get_team(username)

    if request.method == 'POST':
        id_player = request.POST.get("player")    
        testtt = query(f"UPDATE PEMAIN SET Nama_Tim = '{nama_tim}' WHERE ID_Pemain = '{id_player}'")

        print(id_player)
        print(testtt)

    return HttpResponseRedirect(reverse('manager:show_teamdetail'))

@csrf_exempt
def add_coach(request):
    context = {}
    username = "amartusewicz2"
    nama_tim = get_team(username)

    if request.method == 'POST':
        id_coach = request.POST.get("coach")    
        query_add = query(f"UPDATE PELATIH SET Nama_Tim = '{nama_tim}' WHERE ID_Pelatih = '{id_coach}'")
        
        print("\nINI HASILNYA YAA")
        print(query_add)
        print(type(query_add))

        if isinstance(query_add, psycopg2.errors.RaiseException):
            msg = extract_string_before_word(str(query_add), "CONTEXT")
            messages.error(request, msg)
            print('ERROR NIH')
            return render(request, 'addpelatih.html', context)

    return HttpResponseRedirect(reverse('manager:show_teamdetail'))

@csrf_exempt
def make_captain(request):
    context = {}

    username = "amartusewicz2"
    nama_tim = get_team(username)

    if request.method == 'POST':
        id_new_captain = request.POST.get("capt") 
        print(request.POST)
        print("DISINI")
        print(id_new_captain)   
        query(f"""
        UPDATE PEMAIN
            SET Is_Captain = 'TRUE'
            WHERE Nama_Tim = '{nama_tim}'
            and ID_Pemain = '{id_new_captain}'
        """)

    return HttpResponseRedirect(reverse('manager:show_teamdetail'))

@csrf_exempt
def delete_pemain(request):
    context = {}

    if request.method == 'POST':
        id_player = request.POST.get("player")    
        query(f"""
        UPDATE PEMAIN
            SET Nama_Tim = NULL
            WHERE ID_Pemain = '{id_player}'
        """)

    return HttpResponseRedirect(reverse('manager:show_teamdetail'))

@csrf_exempt
def delete_pelatih(request):
    context = {}

    if request.method == 'POST':
        id_coach = request.POST.get("coach")

        query(f"""
            UPDATE PELATIH
                SET Nama_Tim = NULL
                WHERE ID_Pelatih = '{id_coach}'
            """)    

        print(cursor)

    return HttpResponseRedirect(reverse('manager:show_teamdetail'))

@csrf_exempt
def get_team(username):
    id_manager = query(f"""
    SELECT id_manajer 
    FROM MANAJER 
    WHERE username='{username}'""")[0]['id_manajer']

    query_get_team = f"""
    SELECT Nama_Tim
        FROM Tim_Manajer
        WHERE ID_Manajer = '{id_manager}'
    """

    the_team = query(query_get_team)

    return the_team[0]['nama_tim']

@csrf_exempt
def extract_string_before_word(string, word):
    split_string = string.split(word)
    if len(split_string) > 1:
        # If the word is found in the string
        return split_string[0]
    else:
        # If the word is not found in the string
        return string