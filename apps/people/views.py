"""
Vistas de la aplicación people
Gestiona estudiantes y profesores
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Estudiante, Profesor
from apps.academic.models import Grado
from django.contrib.auth import get_user_model
from apps.accounts.views import requerido_login, estudiante_no_editable


User = get_user_model()


# ================= ESTUDIANTE =================

@requerido_login
def estudiante_list(request):
    """Lista todos los estudiantes"""
    estudiante_list = Estudiante.objects.all().order_by('apellido', 'nombre')
    
    # Filtros
    id_grado = request.GET.get('grado')
    if id_grado:
        estudiante_list = estudiante_list.filter(id_grado_id=id_grado)
    
    buscar = request.GET.get('buscar')
    if buscar:
        estudiante_list = estudiante_list.filter(
            Q(codigo_estudiante__icontains=buscar) |
            Q(nombre__icontains=buscar) |
            Q(apellido__icontains=buscar) |
            Q(correo__icontains=buscar)
        )
    
    paginator = Paginator(estudiante_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    grados = Grado.objects.all()
    context = {'page_obj': page_obj, 'grades': grados}
    return render(request, 'people/estudiante_list.html', context)


@requerido_login
def estudiante_detail(request, pk):
    """Muestra el detalle de un estudiante"""
    estudiante = get_object_or_404(Estudiante, pk=pk)
    context = {'estudiante': estudiante}
    return render(request, 'people/estudiante_detail.html', context)


from apps.accounts.views import estudiante_no_editable
@requerido_login
@estudiante_no_editable
def estudiante_create(request):
    """Crea un nuevo estudiante"""
    if request.method == 'POST':
        codigo_estudiante = request.POST.get('codigo_estudiante')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        id_grado_id = request.POST.get('id_grado')
        
        if Estudiante.objects.filter(codigo_estudiante=codigo_estudiante).exists():
            messages.error(request, 'Ya existe un estudiante con este código')
            return redirect('estudiante_create')
        
        Estudiante.objects.create(
            codigo_estudiante=codigo_estudiante,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento or None,
            direccion=direccion,
            telefono=telefono,
            correo=correo,
            id_grado_id=id_grado_id if id_grado_id else None,
        )
        
        messages.success(request, 'Estudiante creado correctamente')
        return redirect('estudiante_list')
    
    grados = Grado.objects.all()
    usuarios = User.objects.filter(is_active=True)
    context = {'grades': grados, 'usuarios': Usuarios}
    return render(request, 'people/estudiante_form.html', context)


@requerido_login
@estudiante_no_editable
def estudiante_edit(request, pk):
    """Edita un estudiante"""
    estudiante = get_object_or_404(Estudiante, pk=pk)
    
    if request.method == 'POST':
        estudiante.codigo_estudiante = request.POST.get('codigo_estudiante')
        estudiante.nombre = request.POST.get('nombre')
        estudiante.apellido = request.POST.get('apellido')
        estudiante.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        estudiante.direccion = request.POST.get('direccion')
        estudiante.telefono = request.POST.get('telefono')
        estudiante.correo = request.POST.get('correo')
        estudiante.id_grado_id = request.POST.get('id_grado') or None
        estudiante.save()
        
        messages.success(request, 'Estudiante actualizado correctamente')
        return redirect('estudiante_list')
    
    grados = Grado.objects.all()
    usuarios = User.objects.filter(is_active=True)
    context = {'estudiante': estudiante, 'grades': grados, 'usuarios': usuarios}
    return render(request, 'people/estudiante_form.html', context)


@requerido_login
@estudiante_no_editable
def estudiante_delete(request, pk):
    """Elimina un estudiante"""
    estudiante = get_object_or_404(Estudiante, pk=pk)
    
    if request.method == 'POST':
        estudiante.delete()
        messages.success(request, 'Estudiante eliminado correctamente')
        return redirect('estudiante_list')
    
    context = {'estudiante': estudiante}
    return render(request, 'people/estudiante_confirm_delete.html', context)


# ================= PROFESOR =================

@requerido_login
def profesor_list(request):
    """Lista todos los profesores"""
    profesor_list = Profesor.objects.all().order_by('apellido', 'nombre')
    
    buscar = request.GET.get('buscar')
    if buscar:
        profesor_list = profesor_list.filter(
            Q(nombre__icontains=buscar) |
            Q(apellido__icontains=buscar) |
            Q(correo__icontains=buscar)
        )
    
    paginator = Paginator(profesor_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'people/profesor_list.html', context)


@requerido_login
def profesor_detail(request, pk):
    """Muestra el detalle de un profesor"""
    profesor = get_object_or_404(Profesor, pk=pk)
    context = {'profesor': profesor}
    return render(request, 'people/profesor_detail.html', context)


@requerido_login
def profesor_create(request):
    """Crea un nuevo profesor"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        especialidad = request.POST.get('especialidad')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        
        Profesor.objects.create(
            nombre=nombre,
            apellido=apellido,
            especialidad=especialidad,
            telefono=telefono,
            correo=correo,
        )
        
        messages.success(request, 'Profesor creado correctamente')
        return redirect('profesor_list')
    
    usuarios = User.objects.filter(is_active=True)
    context = {'usuarios': usuarios}
    return render(request, 'people/profesor_form.html', context)


@requerido_login
def profesor_edit(request, pk):
    """Edita un profesor"""
    profesor = get_object_or_404(Profesor, pk=pk)
    
    if request.method == 'POST':
        profesor.nombre = request.POST.get('nombre')
        profesor.apellido = request.POST.get('apellido')
        profesor.especialidad = request.POST.get('especialidad')
        profesor.telefono = request.POST.get('telefono')
        profesor.correo = request.POST.get('correo')
        profesor.save()
        
        messages.success(request, 'Profesor actualizado correctamente')
        return redirect('profesor_list')
    
    usuarios = User.objects.filter(is_active=True)
    context = {'profesor': profesor, 'usuarios': usuarios}
    return render(request, 'people/profesor_form.html', context)


@requerido_login
def profesor_delete(request, pk):
    """Elimina un profesor"""
    profesor = get_object_or_404(Profesor, pk=pk)
    
    if request.method == 'POST':
        profesor.delete()
        messages.success(request, 'Profesor eliminado correctamente')
        return redirect('profesor_list')
    
    context = {'profesor': profesor}
    return render(request, 'people/profesor_confirm_delete.html', context)