"""
Vistas de la aplicación accounts
Maneja autenticación y gestión de usuarios
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from .models import Rol, Usuario


# ================= AUTENTICACIÓN =================

def login_view(request):
    """Vista de inicio de sesión"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            usuario = Usuario.objects.get(username=username)
            
            # Verificar contraseña hasheada
            if check_password(password, usuario.password):
                if usuario.estado == 'activo':
                    # Guardar usuario en sesión
                    request.session['usuario_id'] = usuario.id
                    request.session['username'] = usuario.username
                    #request.session['rol'] = usuario.id_rol.nombre_rol if usuario.id_rol else ''
                    
                    messages.success(request, f'Bienvenido {usuario.username}')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Usuario inactivo')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no existe')
        
        return redirect('login')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Vista de cierre de sesión"""
    request.session.flush()
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')


def registro_view(request):
    """Crea un nuevo usuario (registro simple)."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        telefono = request.POST.get('telefono')
        id_rol_id = request.POST.get('id_rol')

        if not username or not password or not confirm_password:
            messages.error(request, 'Completa todos los campos requeridos')
            return redirect('registro')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('registro')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return redirect('registro')

        usuario = Usuario.objects.create(
            username=username,
            password=make_password(password),
            telefono=telefono or '',
            estado='activo',
            id_rol_id=id_rol_id if id_rol_id else None,
        )

        messages.success(request, f'Usuario creado: {usuario.username}')
        return redirect('login')

    roles = Rol.objects.all().order_by('nombre_rol')
    return render(request, 'accounts/registro.html', {'roles': roles})



def requerido_login(view_func):
    """Decorador para requerir login (usa la sesión manual del proyecto)."""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            messages.warning(request, 'Debe iniciar sesión')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper



@requerido_login
def dashboard(request):
    """Dashboard principal"""
    context = {
        'username': request.session.get('username'),
    }
    return render(request, 'accounts/dashboard.html', context)


# ================= USUARIOS =================

@requerido_login
def usuario_list(request):
    """Lista todos los usuarios"""
    usuario_list = Usuario.objects.all().order_by('username')
    
    # Filtros
    estado = request.GET.get('estado')
    if estado:
        usuario_list = usuario_list.filter(estado=estado)
    
    id_rol = request.GET.get('rol')
    if id_rol:
        usuario_list = usuario_list.filter(id_rol_id=id_rol)
    
    # Búsqueda
    buscar = request.GET.get('buscar')
    if buscar:
        usuario_list = usuario_list.filter(
            Q(username__icontains=buscar)
        )
    
    paginator = Paginator(usuario_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    roles = Rol.objects.all()
    context = {'page_obj': page_obj, 'roles': roles}
    return render(request, 'accounts/usuario_list.html', context)


@requerido_login
def usuario_detail(request, pk):
    """Muestra el detalle de un usuario"""
    usuario = get_object_or_404(Usuario, pk=pk)
    context = {'usuario': usuario}
    return render(request, 'accounts/usuario_detail.html', context)


@requerido_login
def usuario_create(request):
    """Crea un nuevo usuario"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        telefono = request.POST.get('telefono')
        id_rol_id = request.POST.get('id_rol')
        
        # Validaciones
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('usuario_create')
        
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return redirect('usuario_create')
        
        # Crear usuario con contraseña hasheada
        usuario = Usuario.objects.create(
            username=username,
            password=make_password(password),
            telefono=telefono,
            id_rol_id=id_rol_id if id_rol_id else None,
        )
        
        messages.success(request, 'Usuario creado correctamente')
        return redirect('usuario_list')
    
    roles = Rol.objects.all()
    context = {'roles': roles}
    return render(request, 'accounts/usuario_form.html', context)


@requerido_login
def usuario_edit(request, pk):
    """Edita un usuario existente"""
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.telefono = request.POST.get('telefono')
        usuario.estado = request.POST.get('estado')
        usuario.id_rol_id = request.POST.get('id_rol')
        
        # Cambiar contraseña si se proporciona
        password = request.POST.get('password')
        if password:
            usuario.password = make_password(password)
        
        usuario.save()
        
        messages.success(request, 'Usuario atualizado correctamente')
        return redirect('usuario_list')
    
    roles = Rol.objects.all()
    context = {'usuario': usuario, 'roles': roles}
    return render(request, 'accounts/usuario_form.html', context)


@requerido_login
def usuario_delete(request, pk):
    """Elimina un usuario"""
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente')
        return redirect('usuario_list')
    
    context = {'usuario': usuario}
    return render(request, 'accounts/usuario_confirm_delete.html', context)


# ================= ROLES =================

@requerido_login
def rol_list(request):
    """Lista todos los roles"""
    rol_list = Rol.objects.all()
    context = {'roles': rol_list}
    return render(request, 'accounts/rol_list.html', context)


@requerido_login
def rol_create(request):
    """Crea un nuevo rol"""
    if request.method == 'POST':
        nombre_rol = request.POST.get('nombre_rol')
        descripcion = request.POST.get('descripcion')
        
        if Rol.objects.filter(nombre_rol=nombre_rol).exists():
            messages.error(request, 'Ya existe este rol')
            return redirect('rol_create')
        
        Rol.objects.create(
            nombre_rol=nombre_rol,
            descripcion=descripcion
        )
        
        messages.success(request, 'Rol creado correctamente')
        return redirect('rol_list')
    
    return render(request, 'accounts/rol_form.html')


@requerido_login
def rol_edit(request, pk):
    """Edita un rol"""
    rol = get_object_or_404(Rol, pk=pk)
    
    if request.method == 'POST':
        rol.nombre_rol = request.POST.get('nombre_rol')
        rol.descripcion = request.POST.get('descripcion')
        rol.save()
        
        messages.success(request, 'Rol atualizado correctamente')
        return redirect('rol_list')
    
    context = {'rol': rol}
    return render(request, 'accounts/rol_form.html', context)


@requerido_login
def rol_delete(request, pk):
    """Elimina un rol"""
    rol = get_object_or_404(Rol, pk=pk)
    
    if request.method == 'POST':
        rol.delete()
        messages.success(request, 'Rol eliminado correctamente')
        return redirect('rol_list')
    
    context = {'rol': rol}
    return render(request, 'accounts/rol_confirm_delete.html', context)