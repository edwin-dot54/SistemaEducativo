from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Grado, Materia


# ================= GRADOS =================

@login_required
def grado_list(request):
    """Lista todos los grados"""
    grado_list = Grado.objects.all().order_by('nivel', 'nombre_grado')
    
    # Filtro por nivel
    nivel = request.GET.get('nivel')
    if nivel:
        grado_list = grado_list.filter(nivel=nivel)
    
    # Filtro por jornada
    jornada = request.GET.get('jornada')
    if jornada:
        grado_list = grado_list.filter(jornada=jornada)
    
    # Búsqueda
    buscar = request.GET.get('buscar')
    if buscar:
        grado_list = grado_list.filter(nombre_grado__icontains=buscar)
    
    paginator = Paginator(grado_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'academic/grado_list.html', context)


@login_required
def grado_detail(request, pk):
    """Muestra el detalle de un grado y sus materias"""
    grado = get_object_or_404(Grado, pk=pk)
    materias = grado.materias.all()
    context = {'grado': grado, 'materias': materias}
    return render(request, 'academic/grado_detail.html', context)


@login_required
def grado_create(request):
    """Crea un nuevo grado"""
    if request.method == 'POST':
        nombre_grado = request.POST.get('nombre_grado')
        nivel = request.POST.get('nivel')
        jornada = request.POST.get('jornada')
        
        # Verificar duplicado
        if Grado.objects.filter(
            nombre_grado=nombre_grado,
            nivel=nivel,
            jornada=jornada
        ).exists():
            messages.error(request, 'Ya existe este grado')
            return redirect('grado_create')
        
        Grado.objects.create(
            nombre_grado=nombre_grado,
            nivel=nivel,
            jornada=jornada
        )
        
        messages.success(request, 'Grado creado correctamente')
        return redirect('grado_list')
    
    return render(request, 'academic/grado_form.html')


@login_required
def grado_edit(request, pk):
    """Edita un grado existente"""
    grado = get_object_or_404(Grado, pk=pk)
    
    if request.method == 'POST':
        grado.nombre_grado = request.POST.get('nombre_grado')
        grado.nivel = request.POST.get('nivel')
        grado.jornada = request.POST.get('jornada')
        grado.save()
        
        messages.success(request, 'Grado actualizado correctamente')
        return redirect('grado_list')
    
    context = {'grado': grado}
    return render(request, 'academic/grado_form.html', context)


@login_required
def grado_delete(request, pk):
    """Elimina un grado"""
    grado = get_object_or_404(Grado, pk=pk)
    
    if request.method == 'POST':
        grado.delete()
        messages.success(request, 'Grado eliminado correctamente')
        return redirect('grado_list')
    
    context = {'grado': grado}
    return render(request, 'academic/grado_confirm_delete.html', context)


# ================= MATERIAS =================

@login_required
def materia_list(request):
    """Lista todas las materias"""
    materia_list = Materia.objects.all().order_by('nombre_materia')
    
    # Filtro por grado
    id_grado = request.GET.get('grado')
    if id_grado:
        materia_list = materia_list.filter(id_grado_id=id_grado)
    
    # Filtro por profesor
    id_profesor = request.GET.get('profesor')
    if id_profesor:
        materia_list = materia_list.filter(id_profesor_id=id_profesor)
    
    # Búsqueda
    buscar = request.GET.get('buscar')
    if buscar:
        materia_list = materia_list.filter(nombre_materia__icontains=buscar)
    
    paginator = Paginator(materia_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    grados = Grado.objects.all()
    context = {'page_obj': page_obj, 'grados': grados}
    return render(request, 'academic/materia_list.html', context)


@login_required
def materia_detail(request, pk):
    """Muestra el detalle de una materia"""
    materia = get_object_or_404(Materia, pk=pk)
    context = {'materia': materia}
    return render(request, 'academic/materia_detail.html', context)


@login_required
def materia_create(request):
    """Crea una nueva materia"""
    if request.method == 'POST':
        nombre_materia = request.POST.get('nombre_materia')
        descripcion = request.POST.get('descripcion')
        intensidad_horaria = request.POST.get('intensidad_horaria')
        id_grado_id = request.POST.get('id_grado')
        id_profesor_id = request.POST.get('id_profesor')
        
        # Validar que el grado exista
        if not id_grado_id:
            messages.error(request, 'Debe seleccionar un grado')
            return redirect('materia_create')
        
        Materia.objects.create(
            nombre_materia=nombre_materia,
            descripcion=descripcion,
            intensidad_horaria=intensidad_horaria,
            id_grado_id=id_grado_id,
            id_profesor_id=id_profesor_id if id_profesor_id else None
        )
        
        messages.success(request, 'Materia creada correctamente')
        return redirect('materia_list')
    
    grados = Grado.objects.all()
    # Importación tardía para evitar errores circulares
    from apps.people.models import Profesor
    profesores = Profesor.objects.all()
    context = {'degrees': grados, 'profesores': profesores}
    return render(request, 'academic/materia_form.html', context)


@login_required
def materia_edit(request, pk):
    """Edita una materia existente"""
    materia = get_object_or_404(Materia, pk=pk)
    
    if request.method == 'POST':
        materia.nombre_materia = request.POST.get('nombre_materia')
        materia.descripcion = request.POST.get('descripcion')
        materia.intensidad_horaria = request.POST.get('intensidad_horaria')
        materia.id_grado_id = request.POST.get('id_grado')
        materia.id_profesor_id = request.POST.get('id_profesor') or None
        materia.save()
        
        messages.success(request, 'Materia actualizada correctamente')
        return redirect('materia_list')
    
    grados = Grado.objects.all()
    from apps.people.models import Profesor
    profesores = Profesor.objects.all()
    context = {'materia': materia, 'degrees': grados, 'profesores': profesores}
    return render(request, 'academic/materia_form.html', context)


@login_required
def materia_delete(request, pk):
    """Elimina una materia"""
    materia = get_object_or_404(Materia, pk=pk)
    
    if request.method == 'POST':
        materia.delete()
        messages.success(request, 'Materia eliminada correctamente')
        return redirect('materia_list')
    
    context = {'materia': materia}
    return render(request, 'academic/materia_confirm_delete.html', context)