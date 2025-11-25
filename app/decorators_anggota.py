from django.shortcuts import redirect
from django.contrib import messages
from .models import UserAnggota 
from functools import wraps

def check_useranggota(function):
    def wrapper(request, *args, **kwargs): 
        useranggota = UserAnggota.objects.get(nip=request.user)
        request.useranggota = useranggota
        if useranggota.photo == None :
            messages.error(request, "Lengkapi data anda terlebih dahulu!")
            return redirect('/acd/profile_dsn')               
        return function(request, *args, **kwargs)
    return wrapper

def anggota_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.last_name != "User Anggota":
            return redirect('/acd/dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view