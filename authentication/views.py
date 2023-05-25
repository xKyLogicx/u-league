from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from utils.query import *
from django.contrib import messages
import uuid
import psycopg2
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse


def homepage(request):
    return render(request, "welcome_page.html")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if verify(request):
            username = str(request.session["username"])
            password = str(request.session["password"])
        else:
            username = str(request.POST["username"])
            password = str(request.POST["password"])

        if not username or not password :
            messages.error(request, "Username atau password salah")
            print('ERROR salah uname/pw')
            return render(request, "login.html")

        print(username, password)

        role = get_role(username)
        print(role)

        if role == "" or role == None:
            if username and password:
                messages.error(request, "Username atau password salah")
                print('ERROR salah login')
                return render(request, "login.html")
            print("gatau dah")
            return render(request, "login.html")
        
        else:
            request.session["username"] = username
            request.session["password"] = password
            request.session["role"] = role
            request.session.set_expiry(0)
            request.session.modified = True
        
  
            print('masuk')
            if role == "Manajer":
                return redirect("/manager/")
            
            elif role == "Panitia":
                return redirect("/panitia/")
            
            elif role == "Penonton":
                return redirect("/penonton/")

        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')  # Ganti 'home' dengan URL tujuan setelah berhasil login
        # else:
        #     error_message = "Username atau password salah."
        #     return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

@csrf_exempt
def register_manager(request):
    if request.method == 'POST':
        username = request.POST.get('ManagerUsernameInput')
        password = request.POST.get('ManagerPasswordInput')
        fname = request.POST.get('ManagerFNameInput')
        lname = request.POST.get('ManagerLNameInput')
        nomor_hp = request.POST.get('ManagerNoHPInput')
        email = request.POST.get('ManagerEmailInput')
        alamat = request.POST.get('ManagerAlamatInput')

        is_mhs = request.POST.get('is_mhs')
        is_dosen = request.POST.get('is_dosen')
        is_tendik = request.POST.get('is_tendik')
        is_alumni = request.POST.get('is_alumni')
        is_umum = request.POST.get('is_umum')

        print("LIHAT YA DIA MASUK POST MANAJER GATAU KNP ya")

        print(username, fname, lname, nomor_hp, email, alamat, is_mhs, is_dosen, is_tendik, is_alumni, is_umum)

        if ((username is None) or (password is None) or (fname is None) or (lname is None)):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'managerlogin.html')
        
        if ((username == "") or (password  == "" ) or (fname  == "") or (lname  == "")):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'managerlogin.html')
        
        if ((nomor_hp is None) or (email is None) or (alamat is None)):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'managerlogin.html')
        
        if ((nomor_hp == "") or (email == "") or (alamat == "")):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'managerlogin.html')
        
        if ((is_mhs is None) and (is_dosen is None) and (is_tendik is None) and (is_alumni is None) and (is_umum is None)):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'managerlogin.html')
        
        if ((is_mhs == "") and (is_dosen == "") and (is_tendik == "") and (is_alumni == "") and (is_umum == "")):
            messages.error(request, "Mohon isi data dengan lengkap.")            
            return render(request, 'managerlogin.html')

        uname_check = insert_user_system(username, password)
        
        if isinstance(uname_check, psycopg2.errors.RaiseException):
            msg = extract_string_before_word(str(uname_check), "CONTEXT")
            messages.error(request, msg)
            print('ERROR UNAME NIH')
            return render(request, 'managerlogin.html')
        
        print("ok sudah insert user system")

        id_non_pemain = str(uuid.uuid4())

        non_pemain = insert_non_pemain(id_non_pemain, fname, lname, nomor_hp, email, alamat)

        insert_status(id_non_pemain, is_mhs, is_dosen, is_tendik, is_alumni, is_umum)

        insert_manajer = query(f"""
            INSERT INTO MANAJER values
            ('{id_non_pemain}', '{username}')
        """)

        print('INI DETAILNYA YA', non_pemain, '\n', insert_manajer, '\n')

        return HttpResponseRedirect(reverse('authentication:login'))

    return render(request, 'managerlogin.html')

@csrf_exempt
def register_panitia(request):
    if request.method == 'POST':
        username = request.POST.get('PanitiaUsernameInput')
        password = request.POST.get('PanitiaPasswordInput')
        fname = request.POST.get('PanitiaFNameInput')
        lname = request.POST.get('PanitiaLNameInput')
        nomor_hp = request.POST.get('PanitiaNoHPInput')
        email = request.POST.get('PanitiaEmailInput')
        alamat = request.POST.get('PanitiaAlamatInput')

        is_mhs = request.POST.get('is_mhs')
        is_dosen = request.POST.get('is_dosen')
        is_tendik = request.POST.get('is_tendik')
        is_alumni = request.POST.get('is_alumni')
        is_umum = request.POST.get('is_umum')

        jabatan = request.POST.get('PanitiaJabatanInput')

        print("LIHAT YA DIA MASUK POST PANITIA GATAU KNP ya")

        print(username, fname, lname, nomor_hp, email, alamat, is_mhs, is_dosen, is_tendik, is_alumni, is_umum)

        if ((username is None) or (password is None) or (fname is None) or (lname is None)):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'panitialogin.html')
        
        if ((username == "") or (password  == "" ) or (fname  == "") or (lname  == "")):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'panitialogin.html')
        
        if ((nomor_hp is None) or (email is None) or (alamat is None) or (jabatan is None)):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'panitialogin.html')
        
        if ((nomor_hp == "") or (email == "") or (alamat == "") or (jabatan == "")):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'panitialogin.html')
        
        if ((is_mhs is None) and (is_dosen is None) and (is_tendik is None) and (is_alumni is None) and (is_umum is None)):
            messages.error(request, "Mohon isi data dengan lengkap.")            
            return render(request, 'panitialogin.html')
        
        if ((is_mhs == "") and (is_dosen == "") and (is_tendik == "") and (is_alumni == "") and (is_umum == "")):
            messages.error(request, "Mohon isi data dengan lengkap.")            
            return render(request, 'panitialogin.html')

        uname_check = insert_user_system(username, password)
        
        if isinstance(uname_check, psycopg2.errors.RaiseException):
            msg = extract_string_before_word(str(uname_check), "CONTEXT")
            messages.error(request, msg)
            print('ERROR UNAME NIH')
            return render(request, 'panitialogin.html')
        
        print("ok sudah insert user system")

        id_non_pemain = str(uuid.uuid4())

        non_pemain = insert_non_pemain(id_non_pemain, fname, lname, nomor_hp, email, alamat)

        insert_status(id_non_pemain, is_mhs, is_dosen, is_tendik, is_alumni, is_umum)

        insert_panitia = query(f"""
            INSERT INTO PANITIA values
            ('{id_non_pemain}', '{jabatan}', '{username}')
        """)

        print('INI DETAILNYA YA', non_pemain, '\n', insert_panitia, '\n')

        return HttpResponseRedirect(reverse('authentication:login'))
    
    return render(request, 'panitialogin.html')

@csrf_exempt
def register_penonton(request):
    if request.method == 'POST':
        username = request.POST.get('PenontonUsernameInput')
        password = request.POST.get('PenontonPasswordInput')
        fname = request.POST.get('PenontonFNameInput')
        lname = request.POST.get('PenontonLNameInput')
        nomor_hp = request.POST.get('PenontonNoHPInput')
        email = request.POST.get('PenontonEmailInput')
        alamat = request.POST.get('PenontonAlamatInput')

        is_mhs = request.POST.get('is_mhs')
        is_dosen = request.POST.get('is_dosen')
        is_tendik = request.POST.get('is_tendik')
        is_alumni = request.POST.get('is_alumni')
        is_umum = request.POST.get('is_umum')

        print("LIHAT YA DIA MASUK POST PENONTON GATAU KNP ya")

        print(username, fname, lname, nomor_hp, email, alamat, is_mhs, is_dosen, is_tendik, is_alumni, is_umum)

        if ((username is None) or (password is None) or (fname is None) or (lname is None)):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'penontonlogin.html')
        
        if ((username == "") or (password  == "" ) or (fname  == "") or (lname  == "")):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'penontonlogin.html')
        
        if ((nomor_hp is None) or (email is None) or (alamat is None)):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'penontonlogin.html')
        
        if ((nomor_hp == "") or (email == "") or (alamat == "")):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'penontonlogin.html')
        
        if ((is_mhs is None) and (is_dosen is None) and (is_tendik is None) and (is_alumni is None) and (is_umum is None)):
            messages.error(request, "Mohon isi data dengan lengkap.")
            return render(request, 'penontonlogin.html')
        
        if ((is_mhs == "") and (is_dosen == "") and (is_tendik == "") and (is_alumni == "") and (is_umum == "")):
            messages.error(request, "Mohon isi data dengan lengkap.")            
            return render(request, 'penontonlogin.html')

        uname_check = insert_user_system(username, password)
        
        if isinstance(uname_check, psycopg2.errors.RaiseException):
            msg = extract_string_before_word(str(uname_check), "CONTEXT")
            messages.error(request, msg)
            print('ERROR UNAME NIH')
            return render(request, 'penontonlogin.html')
        
        print("ok sudah insert user system")

        id_non_pemain = str(uuid.uuid4())

        non_pemain = insert_non_pemain(id_non_pemain, fname, lname, nomor_hp, email, alamat)

        insert_status(id_non_pemain, is_mhs, is_dosen, is_tendik, is_alumni, is_umum)

        insert_penonton = query(f"""
            INSERT INTO PENONTON values
            ('{id_non_pemain}', '{username}')
        """)

        print('INI DETAILNYA YA', non_pemain, '\n', insert_penonton, '\n')

        return HttpResponseRedirect(reverse('authentication:login'))
    
    return render(request, 'penontonlogin.html')

def logout(request):
    request.session.flush()
    request.session.clear_expired()
    print("BERHASIL LOGOUT HARUSNYA")
    return render(request, "welcome_page.html")

def register_view(request):
    return render(request, "register.html")

@csrf_exempt
def register_form(request):
    return render(request, 'register.html')

def verify(request):
    try:
        request.session["username"]
        return True
    except:
        return False
    
def get_role(username):
    res = query(f"SELECT * FROM MANAJER WHERE username='{username}'")
    if len(res) > 0:
        return "Manajer"
    
    res = query(f"SELECT * FROM PANITIA WHERE username='{username}'")
    if len(res) > 0:
        return "Panitia"
    
    res = query(f"SELECT * FROM PENONTON WHERE username='{username}'")
    if len(res) > 0:
        return "Penonton"
    
def insert_user_system(uname, pw):
    hasil = query(f"""
        INSERT INTO USER_SYSTEM values
        ('{uname}', '{pw}')
    """)
    return hasil

def insert_non_pemain(id_non_pemain, nama_depan, nama_blkg, nomor_hp, email, alamat):
    hasil = query(f"""
        INSERT INTO NON_PEMAIN values
        ('{id_non_pemain}', '{nama_depan}', '{nama_blkg}', {nomor_hp}, '{email}', '{alamat}')
    """)
    return hasil

def insert_status(id_non_pemain, is_mhs, is_dosen, is_tendik, is_alumni, is_umum):
    if is_mhs is not None:
        print("MHS NOT NONE")

        query(f"""
            INSERT INTO STATUS_NON_PEMAIN values
            ('{id_non_pemain}', 'Mahasiswa')
        """)
    
    if is_dosen is not None:
        print("DOSEN NOT NONE")

        query(f"""
            INSERT INTO STATUS_NON_PEMAIN values
            ('{id_non_pemain}', 'Dosen')
        """)

    if is_tendik is not None:
        print("TENDIK NOT NONE")

        query(f"""
            INSERT INTO STATUS_NON_PEMAIN values
            ('{id_non_pemain}', 'Tendik')
        """)
    
    if is_alumni is not None:
        print("ALUMNI NOT NONE")

        query(f"""
            INSERT INTO STATUS_NON_PEMAIN values
            ('{id_non_pemain}', 'Alumni')
        """)
    
    if is_umum is not None:
        print("UMUM NOT NONE")

        query(f"""
            INSERT INTO STATUS_NON_PEMAIN values
            ('{id_non_pemain}', 'Umum')
        """)

def extract_string_before_word(string, word):
    split_string = string.split(word)
    if len(split_string) > 1:
        # If the word is found in the string
        return split_string[0]
    else:
        # If the word is not found in the string
        return string