"""
Vistas de la aplicación attendance
Gestiona la asistencia de estudiantes
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Asistencia
from apps.people.models import Estudiante
from apps.accounts.views import requerido_login


@requerido_login
def asistencia_list(request):
    """Lista todas las asistencia"""
    asistencia_list = Asistencia.objects.all().order_by('-fecha')
    
    # Filtros
    fecha = request.GET.get('fecha')
    if fecha:
        asistencia_list = asistencia_list.filter(fecha=fecha)
    
    estado = request.GET.get('estado')
    if estado:
        asistencia_list = asistencia_list.filter(estado=estado)
    
    # Búsqueda por estudiante
    id_estudiante = request.GET.get('estudiante')
    if id_estudiante:
        asistencia_list = asistencia_list.filter(id_estudiante_id=id_estudiante)
    
    paginator = Paginator(asistencia_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    estudiantes = Estudiante.objects.all()
    context = {'page_obj': page_obj, 'estudiantes': estudiantes}
    return render(request, 'attendance/asistencia_list.html', context)


@requerido_login
def asistencia_detail(request, pk):
    """Muestra el detalle de una asistencia"""
    asistencia = get_object_or_404(Asistencia, pk=pk)
    context = {'asistencia': asistencia}
    return render(request, 'attendance/asistencia_detail.html', context)


@requerido_login
def asistencia_create(request):
    """Registra una nueva asistencia"""
    if request.method == 'POST':
        id_estudiante_id = request.POST.get('id_estudiante')
        fecha = request.POST.get('fecha')
        estado = request.POST.get('estado')
        observacion = request.POST.get('observacion')
        
        # Verificar si ya existe registro
        if Asistencia.objects.filter(id_estudiante_id=id_estudiante_id, fecha=fecha).exists():
            messages.error(request, 'Ya existe registro de asistencia para este estudiante en esta fecha')
            return redirect('asistencia_create')
        
        Asistencia.objects.create(
            id_estudiante_id=id_estudiante_id,
            fecha=fecha,
            estado=estado,
            observacion=observacion,
        )
        
        messages.success(request, 'Asistencia registrada correctamente')
        return redirect('asistencia_list')
    
    estudiantes = Estudiante.objects.all()
    context = {'estudiantes': estudiantes}
    return render(request, 'attendance/asistencia_form.html', context)


@requerido_login
def asistencia_edit(request, pk):
    """Edita una asistencia"""
    asistencia = get_object_or_404(Asistencia, pk=pk)
    
    if request.method == 'POST':
        asistencia.id_estudiante_id = request.POST.get('id_estudiante')
        asistencia.fecha = request.POST.get('fecha')
        asistencia.estado = request.POST.get('estado')
        asistencia.observacion = request.POST.get('observacion')
        asistencia.save()
        
        messages.success(request, 'Asistencia actualizada correctamente')
        return redirect('asistencia_list')
    
    estudiantes = Estudiante.objects.all()
    context = {'asistencia': asistencia, 'estudiantes': estudiantes}
    return render(request, 'attendance/asistencia_form.html', context)


@requerido_login
def asistencia_delete(request, pk):
    """Elimina una asistencia"""
    asistencia = get_object_or_404(Asistencia, pk=pk)
    
    if request.method == 'POST':
        asistencia.delete()
        messages.success(request, 'Asistencia eliminada correctamente')
        return redirect('asistencia_list')
    
    context = {'asistencia': asistencia}
    return render(request, 'attendance/asistencia_confirm_delete.html', context)


@requerido_login
def asistencia_fecha(request, fecha):
    """Lista asistencia por fecha específica"""
    asistencia_list = Asistencia.objects.filter(fecha=fecha).order_by('id_estudiante')
    
    context = {
        'asistencia_list': asistencia_list,
        'fecha': fecha,
    }
    return render(request, 'attendance/asistencia_fecha.html', context)