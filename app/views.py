from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserAnggota, UserAdmin
from datetime import date
from django.contrib import messages
from django.http import HttpResponse


@login_required
def index(request):

    userC = None # izin menambahkan userC = None
    data = None

    if request.user.last_name == 'User Anggota':  
        try:
            userC = UserAnggota.objects.get(nip=request.user)
        except UserAnggota.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/dashboard/anggota/profile')
    elif request.user.last_name == 'User Admin':  
        try:
            userC = UserAdmin.objects.get(username=request.user)
        except UserAdmin.DoesNotExist:
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/dashboard/admin/profile')    
    context = {
        'title' : 'Dashboard',
        'heading' : 'Dashboard',
        'photo' : userC.photo if userC else None,
        'userdetail' : userC if userC else None,
        'data' : data,
    }
    
    if request.user.last_name == "User Admin":
        return render(request,'admin_managed/index.html', context)
    elif request.user.last_name == "User Anggota":
        return render(request,'anggota_managed/index.html', context)
    else:
        return HttpResponse("Hello, world!")