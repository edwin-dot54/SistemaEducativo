"""
Vistas de la aplicación assignments
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Tarea
from apps.academic.models import Materia
from apps.people.models import Profesor


# ================= TAREA =================

@login_required
def tarea_list(request):
    """Lista todas las tareas"""
    tarea_list = Tarea.objects.all().order_by('-created_at')
    
    # Filtros
    id_materia = request.GET.get('materia')
    if id_materia:
        tarea_list = tarea_list.filter(id_materia_id=id_materia)
    
    id_profesor = request.GET.get('profesor')
    if id_profesor:
        tarea_list = tarea_list.filter(id_profesor_id=id_profesor)
    
    # Búsqueda
    buscar = request.GET.get('buscar')
    if buscar:
        tarea_list = tarea_list.filter(
            Q(titulo__icontains=buscar) |
            Q(descripcion__icontains=buscar)
        )
    
    paginator = Paginator(tarea_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    context = {'page_obj': page_obj, 'materias': materias, 'profesores': profesores}
    return render(request, 'assignments/tarea_list.html', context)


@login_required
def tarea_detail(request, pk):
    """Muestra el detalle de una tarea"""
    tarea = get_object_or_404(Tarea, pk=pk)
    context = {'tarea': tarea}
    return render(request, 'assignments/tarea_detail.html', context)


@login_required
def tarea_create(request):
    """Crea una nueva tarea"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_entrega = request.POST.get('fecha_entrega')
        id_materia_id = request.POST.get('id_materia')
        id_profesor_id = request.POST.get('id_profesor')
        
        if not id_materia_id:
            messages.error(request, 'Debe seleccionar una materia')
            return redirect('tarea_create')
        
        if not id_profesor_id:
            messages.error(request, 'Debe seleccionar un profesor')
            return redirect('tarea_create')
        
        Tarea.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha_entrega=fecha_entrega,
            id_materia_id=id_materia_id,
            id_profesor_id=id_profesor_id,
        )
        
        messages.success(request, 'Tarea creada correctamente')
        return redirect('tarea_list')
    
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    context = {'materias': materies, 'profesores': professors}
    return render(request, 'assignments/tarea_form.html', context)


@login_required
def tarea_edit(request, pk):
    """Edita una tarea"""
    tarea = get_object_or_404(Tarea, pk=pk)
    
    if request.method == 'POST':
        tarea.titulo = request.POST.get('titulo')
        tarea.descripcion = request.POST.get('descripcion')
        tarea.fecha_entrega = request.POST.get('fecha_entrega')
        tarea.id_materia_id = request.POST.get('id_materia')
        tarea.id_profesor_id = request.POST.get('id_profesor')
        tarea.save()
        
        messages.success(request, 'Tarea actualizada correctamente')
        return redirect('tarea_list')
    
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    context = {'tarea': tarea, 'materias': materies, 'profesores': professors}
    return render(request, 'assignments/tarea_form.html', context)


@login_required
def tarea_delete(request, pk):
    """Elimina una tarea"""
    tarea = get_object_or_404(Tarea, pk=pk)
    
    if request.method == 'POST':
        tarea.delete()
        messages.success(request, 'Tarea eliminada correctamente')
        return redirect('tarea_list')
    
    context = {'tarea': tarea}
    return render(request, 'assignments/tarea_confirm_delete.html', context)