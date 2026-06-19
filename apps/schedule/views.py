"""
Vistas de la aplicación schedule
Gestiona los horarios de clases
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Horario
from apps.academic.models import Grado, Materia
from apps.accounts.views import requerido_login


@requerido_login
def horario_list(request):
    """Lista todos los horarios"""
    horario_list = Horario.objects.all().order_by('id_grado', 'dia_semana', 'hora_inicio')
    
    # Filtros
    id_grado = request.GET.get('grado')
    if id_grado:
        horario_list = horario_list.filter(id_grado_id=id_grado)
    
    id_materia = request.GET.get('materia')
    if id_materia:
        horario_list = horario_list.filter(id_materia_id=id_materia)
    
    dia_semana = request.GET.get('dia')
    if dia_semana:
        horario_list = horario_list.filter(dia_semana=dia_semana)
    
    buscar = request.GET.get('buscar')
    if buscar:
        horario_list = horario_list.filter(
            Q(id_grado__nombre_grado__icontains=buscar) |
            Q(id_materia__nombre_materia__icontains=buscar)
        )
    
    paginator = Paginator(horario_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    grados = Grado.objects.all()
    materias = Materia.objects.all()
    context = {
        'page_obj': page_obj,
        'grados': grados,
        'materias': materias
    }
    return render(request, 'schedule/horario_list.html', context)


@requerido_login
def horario_detail(request, pk):
    """Muestra el detalle de un horario"""
    horario = get_object_or_404(Horario, pk=pk)
    context = {'horario': horario}
    return render(request, 'schedule/horario_detail.html', context)


@requerido_login
def horario_create(request):
    """Crea un nuevo horario"""
    if request.method == 'POST':
        id_grado_id = request.POST.get('id_grado')
        id_materia_id = request.POST.get('id_materia')
        dia_semana = request.POST.get('dia_semana')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        aula = request.POST.get('aula')
        
        # Verificar conflicto de horario
        if Horario.objects.filter(
            id_grado_id=id_grado_id,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio
        ).exists():
            messages.error(request, 'Ya existe un horario para este grado, día y hora')
            return redirect('horario_create')
        
        Horario.objects.create(
            id_grado_id=id_grado_id,
            id_materia_id=id_materia_id,
            dia_semana=dia_semana,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            aula=aula,
        )
        
        messages.success(request, 'Horario creado correctamente')
        return redirect('horario_list')
    
    grados = Grado.objects.all()
    materias = Materia.objects.all()
    context = {'grados': grados, 'materias': materias}
    return render(request, 'schedule/horario_form.html', context)


@requerido_login
def horario_edit(request, pk):
    """Edita un horario"""
    horario = get_object_or_404(Horario, pk=pk)
    
    if request.method == 'POST':
        horario.id_grado_id = request.POST.get('id_grado')
        horario.id_materia_id = request.POST.get('id_materia')
        horario.dia_semana = request.POST.get('dia_semana')
        horario.hora_inicio = request.POST.get('hora_inicio')
        horario.hora_fin = request.POST.get('hora_fin')
        horario.aula = request.POST.get('aula')
        horario.save()
        
        messages.success(request, 'Horario actualizado correctamente')
        return redirect('horario_list')
    
    grados = Grado.objects.all()
    materias = Materia.objects.all()
    context = {'horario': horario, 'grado': grados, 'materias': materias}
    return render(request, 'schedule/horario_form.html', context)


@requerido_login
def horario_delete(request, pk):
    """Elimina un horario"""
    horario = get_object_or_404(Horario, pk=pk)
    
    if request.method == 'POST':
        horario.delete()
        messages.success(request, 'Horario eliminado correctamente')
        return redirect('horario_list')
    
    context = {'horario': horario}
    return render(request, 'schedule/horario_confirm_delete.html', context)


@requerido_login
def horario_por_grado(request, pk):
    """Muestra el horario de un grado específico"""
    grado = get_object_or_404(Grado, pk=pk)
    horario_list = Horario.objects.filter(id_grado_id=pk).order_by('dia_semana', 'hora_inicio')
    
    # Agrupar por día
    horarios_por_dia = {}
    for h in horario_list:
        if h.dia_semana not in horarios_por_dia:
            horarios_por_dia[h.dia_semana] = []
        horarios_por_dia[h.dia_semana].append(h)
    
    context = {
        'grado': grado,
        'horarios_por_dia': horarios_por_dia
    }
    return render(request, 'schedule/horario_por_grado.html', context)
