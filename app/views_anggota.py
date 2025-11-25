from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models import Q
from django.forms import inlineformset_factory
from django.contrib.auth import update_session_auth_hash
import uuid
from uuid import UUID
from .models import UserAnggota
from .forms_anggota import formProfile, formResetPasswordAnggota
from .decorators_anggota import anggota_required, check_useranggota


@anggota_required
def profile_anggota(request):
    userdosen = UserAnggota.objects.get(nip=request.user)     
    if request.method == 'POST':
        form = formProfile(request.POST, request.FILES, instance=userdosen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('/dashboard/profile/dosen')
    else:
        form = formProfile(instance=userdosen)

    context = {
        'title' : 'Profile',
        'heading' : 'Edit Profile',
        'userdosen' : userdosen,
        'photo' : userdosen.photo,
        'form': form,
    }
    return render(request, 'anggota/set/profile.html', context)


@check_useranggota
@anggota_required
def reset_password_anggota(request):
    if request.method == 'POST':
        form = formResetPasswordAnggota(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            
            # Verifikasi password saat ini
            if not request.user.check_password(current_password):
                messages.error(request, 'Password saat ini tidak benar!')
                return render(request, 'dosen/reset_password.html', {'form': form})
            
            # Update password
            request.user.set_password(new_password)
            request.user.save()

            # Pertahankan sesi login
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Password berhasil diubah!')
            return redirect('app:dashboard')  # langsung redirect tanpa login ulang
    else:
        form = formResetPasswordAnggota()
    
    context = {
        'form': form,
        'title': 'Reset Password',
        'heading': 'Reset Password',
    }
    return render(request, 'anggota/reset_password.html', context)
