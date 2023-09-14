from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
import json


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username , password = password)
        if user:
            if user.is_active:
                login(request, user)
                if user.userprofile.role == 'kasir':
                    return redirect('indexKasir')
                elif user.userprofile.role == 'admin':
                     return redirect('indexAdmin')
        else:
            return render(request , 'Login.html')
    else:
        return render(request , 'Login.html')

def logout_view(request):
    logout(request)
    return redirect('login_view')

#admin

@login_required
def indexAdmin(request):
        if request.user.userprofile.role != 'admin':
             return redirect('login_view')
        return render(request, 'Admin/index.html')


def tambahMenu(request):
     return render(request, 'Admin/tambahMenu.html')

def editMenu(request):
     return render(request, 'Admin/editMenu.html')

def hapusMenu(request):
     return render(request, 'Admin/hapusMenu.html')

@login_required
def laporanAdmin(request):
        if request.user.userprofile.role != 'admin':
             return redirect('login_view')
        return render(request, 'Admin/laporanAdmin.html')


#Kasir
@login_required
def indexKasir(request):
        if request.user.userprofile.role != 'kasir':
            return redirect('login_view')
        return render(request, 'Kasir/index.html')

def kasiran(request):
     return render(request, 'Kasir/kasiran.html')

def pesanan(request):
     return render(request, 'kasir/pesanan.html')

def tabelKasir(request):
     return render(request, 'kasir/tabelKasir.html')

#User
@login_required
def indexUser(request):
    return render(request, 'User/index.html')