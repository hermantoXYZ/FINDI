from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib import messages

from .models import UserAdmin, UserAnggota
from django.contrib.auth.models import User

from .forms_admin import formProfile, formUserEdit
from .decorators_admin import admin_required, check_useradmin

########### SET PROFILE #####################################################

@admin_required
def profile_admin(request):
    userprodi = UserAdmin.objects.get(username=request.user)      
    if request.method == 'POST':
        form = formProfile(request.POST,  request.FILES, instance=userprodi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/dashboard/profile/admin')
    else:
        form = formProfile(instance=userprodi)

    context = {
        'title' : 'Profile',
        'heading' : 'Edit Profile',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'form': form,
    }
    return render(request, 'admin_managed/set/profile.html', context)



########### SETTING USER LAIN #####################################################

@check_useradmin
@admin_required
def user_list(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Password tidak cocok.")
        else:
            user = get_object_or_404(User, id=user_id)
            user.set_password(new_password)
            user.save()
            messages.success(request, f"Password untuk {user.username} berhasil diganti.")
            
    useradmin = request.useradmin
    role = request.GET.get('role', 'User Anggota')
    
    if role == 'Admin':
        user_data = UserAdmin.objects.all()
    elif role == 'Anggota':
        user_data = UserAnggota.objects.all()
    else:
        # fallback supaya tidak error
        user_data = []
        messages.warning(request, f"Role '{role}' tidak dikenali.")

    context = {
        'title': 'User List',
        'heading': role,
        'userprodi' : useradmin,
        'photo' : useradmin.photo,
        'user_data': user_data,
    }
    return render(request, 'admin_managed/set/user_list.html', context)



@check_useradmin
@admin_required
def user_edit(request, id, role):
    userprodi = request.userprodi  
    userMaster = get_object_or_404(User, username=id)
    if role == 'User Anggota':
        userSelect = get_object_or_404(UserAnggota, nim=id)
    if role == 'User Admin':
        userSelect = get_object_or_404(UserAdmin, nip=id)
    if request.method == 'POST':
        form = formUserEdit(request.POST, request.FILES, instance=userSelect)
        if form.is_valid():
            userSelect.save()  
            messages.success(request, 'Update User Berhasil')
            if role == 'User Anggota':
                return redirect('app:user_edit', userSelect.nim_id, role)
            else:
                return redirect('app:user_edit', userSelect.nip_id, role)
        else:
            messages.error(request, 'periksa kembali isian data anda!')
            if role == 'User Admin':
                return redirect('app:user_edit', userSelect.nim_id, role)
            else:
                return redirect('app:user_edit', userSelect.nip_id, role)

    else:
        form = formUserEdit(instance=userSelect)

    context = {
        'title' : 'Edit User',
        'heading' : 'Edit User',
        'userprodi' : userprodi,
        'photo' : userprodi.photo,
        'userselect' : userSelect,
        'usermaster' : userMaster,
        'form': form,
    }
    return render(request, 'prodi/set/user_edit.html', context)