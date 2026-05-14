from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesion para acceder.')
            return redirect('login')
        
        if not request.user.is_staff and not request.user.groups.filter(name='Administrador').exists():
            messages.error(request, 'Solo los administradores pueden acceder a esta pagina.')
            return redirect('lista_candidatas')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def jury_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesion para acceder.')
            return redirect('login')
        
        is_admin = request.user.is_staff or request.user.groups.filter(name='Administrador').exists()
        is_jury = request.user.groups.filter(name='Jurado').exists()
        
        if not is_admin and not is_jury:
            messages.error(request, 'No tienes permisos para acceder.')
            return redirect('lista_candidatas')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def get_user_role(request):
    if not request.user.is_authenticated:
        return None
    
    if request.user.is_staff or request.user.groups.filter(name='Administrador').exists():
        return 'administrador'
    
    if request.user.groups.filter(name='Jurado').exists():
        return 'jurado'
    
    return None

def can_edit_candidata(request):
    return request.user.is_authenticated and (
        request.user.is_staff or 
        request.user.groups.filter(name='Administrador').exists()
    )

def can_delete_candidata(request):
    return request.user.is_authenticated and (
        request.user.is_staff or 
        request.user.groups.filter(name='Administrador').exists()
    )

def can_reset_scores(request):
    return request.user.is_authenticated and (
        request.user.is_staff or 
        request.user.groups.filter(name='Administrador').exists()
    )