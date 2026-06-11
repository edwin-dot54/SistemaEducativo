"""
Vistas de la aplicación grades
Gestiona las calificaciones de estudiantes
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Nota
from apps.people.models import Estudiante
from apps.academic.models import Materia


@login_required
def nota_list(request):
    """Lista todas las notas"""
    nota_list = Nota.objects.all().order_by('-fecha_registro')
    
    # Filtros
    id_estudiante = request.GET.get('estudiante')
    if id_estudiante:
        nota_list = nota_list.filter(id_estudiante_id=id_estudiante)
    
    id_materia = request.GET.get('materia')
    if id_materia:
        nota_list = nota_list.filter(id_materia_id=id_materia)
    
    periodo = request.GET.get('periodo')
    if periodo:
        nota_list = nota_list.filter(periodo=periodo)
    
    estudiante_id = request.GET.get('buscar')
    if estudiante_id:
        nota_list = nota_list.filter(
            Q(id_estudiante__nombre__icontains=estudiante_id) |
            Q(id_estudiante__apellido__icontains=estudiante_id)
        )
    
    paginator = Paginator(nota_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    estudiantes = Estudiante.objects.all()
    materias = Materia.objects.all()
    context = {
        'page_obj': page_obj,
        'estudiantes': estudiantes,
        'materias': materias
    }
    return render(request, 'grades/nota_list.html', context)


@login_required
def nota_detail(request, pk):
    """Muestra el detalle de una nota"""
    nota = get_object_or_404(Nota, pk=pk)
    context = {'nota': nota}
    return render(request, 'grades/nota_detail.html', context)


@login_required
def nota_create(request):
    """Registra una nueva nota"""
    if request.method == 'POST':
        id_estudiante_id = request.POST.get('id_estudiante')
        id_materia_id = request.POST.get('id_materia')
        periodo = request.POST.get('periodo')
        nota = request.POST.get('nota')
        observacion = request.POST.get('observacion')
        
        # Verificar si ya existe registro
        if Nota.objects.filter(
            id_estudiante_id=id_estudiante_id,
            id_materia_id=id_materia_id,
            periodo=periodo
        ).exists():
            messages.error(request, 'Ya existe nota para este estudiante en esta materia y período')
            return redirect('nota_create')
        
        Nota.objects.create(
            id_estudiante_id=id_estudiante_id,
            id_materia_id=id_materia_id,
            periodo=periodo,
            nota=nota,
            observacion=observacion,
        )
        
        messages.success(request, 'Nota registrada correctamente')
        return redirect('nota_list')
    
    estudiantes = Estudiante.objects.all()
    materias = Materia.objects.all()
    context = {'estudiantes': estudiantes, 'materias': materias}
    return render(request, 'grades/nota_form.html', context)


@login_required
def nota_edit(request, pk):
    """Edita una nota"""
    nota = get_object_or_404(Nota, pk=pk)
    
    if request.method == 'POST':
        nota.id_estudiante_id = request.POST.get('id_estudiante')
        nota.id_materia_id = request.POST.get('id_materia')
        nota.periodo = request.POST.get('periodo')
        nota.nota = request.POST.get('nota')
        nota.observacion = request.POST.get('observacion')
        nota.save()
        
        messages.success(request, 'Nota actualizada correctamente')
        return redirect('nota_list')
    
    estudiantes = Estudiante.objects.all()
    materias = Materia.objects.all()
    context = {'nota': nota, 'estudiantes': estudiantes, 'materias': materias}
    return render(request, 'grades/nota_form.html', context)


@login_required
def nota_delete(request, pk):
    """Elimina una nota"""
    nota = get_object_or_404(Nota, pk=pk)
    
    if request.method == 'POST':
        nota.delete()
        messages.success(request, 'Nota eliminada correctamente')
        return redirect('nota_list')
    
    context = {'nota': nota}
    return render(request, 'grades/nota_confirm_delete.html', context)