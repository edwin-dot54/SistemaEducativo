"""
Vistas de la aplicación payments
Gestiona los pagos de estudiantes
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import Pago
from apps.people.models import Estudiante
from apps.accounts.views import requerido_login, estudiante_no_editable




@requerido_login
def pago_list(request):
    """Lista todos los pagos"""
    pago_list = Pago.objects.all().order_by('-id')
    
    # Filtros
    id_estudiante = request.GET.get('estudiante')
    if id_estudiante:
        pago_list = pago_list.filter(id_estudiante_id=id_estudiante)
    
    concepto = request.GET.get('concepto')
    if concepto:
        pago_list = pago_list.filter(concepto=concepto)
    
    estado = request.GET.get('estado')
    if estado:
        pago_list = pago_list.filter(estado=estado)
    
    # Búsqueda
    buscar = request.GET.get('buscar')
    if buscar:
        pago_list = pago_list.filter(
            Q(id_estudiante__nombre__icontains=buscar) |
            Q(id_estudiante__apellido__icontains=buscar)
        )
    
    # Totales
    total_pendiente = Pago.objects.filter(estado='pendiente').aggregate(Sum('monto'))['monto__sum'] or 0
    total_pagado = Pago.objects.filter(estado='pagado').aggregate(Sum('monto'))['monto__sum'] or 0
    
    paginator = Paginator(pago_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    estudiantes = Estudiante.objects.all()
    context = {
        'page_obj': page_obj,
        'estudiantes': estudiantes,
        'total_pendiente': total_pendiente,
        'total_pagado': total_pagado
    }
    return render(request, 'payments/pago_list.html', context)


@requerido_login
def pago_detail(request, pk):
    """Muestra el detalle de un pago"""
    pago = get_object_or_404(Pago, pk=pk)
    context = {'pago': pago}
    return render(request, 'payments/pago_detail.html', context)


@requerido_login
def pago_create(request):
    """Registra un nuevo pago"""
    if request.method == 'POST':
        id_estudiante_id = request.POST.get('id_estudiante')
        concepto = request.POST.get('concepto')
        monto = request.POST.get('monto')
        fecha_pago = request.POST.get('fecha_pago')
        metodo_pago = request.POST.get('metodo_pago')
        estado = request.POST.get('estado', 'pendiente')

        if not metodo_pago:
            metodo_pago = 'efectivo'

        Pago.objects.create(
            id_estudiante_id=id_estudiante_id,
            concepto=concepto,
            monto=monto,
            fecha_pago=fecha_pago,
            metodo_pago=metodo_pago,
            estado=estado,
        )
        
        messages.success(request, 'Pago registrado correctamente')
        return redirect('pago_list')
    
    estudiantes = Estudiante.objects.all()
    context = {'estudiantes': estudiantes}
    return render(request, 'payments/pago_form.html', context)


@requerido_login
@estudiante_no_editable
def pago_edit(request, pk):
    """Edita un pago"""
    pago = get_object_or_404(Pago, pk=pk)
    
    if request.method == 'POST':
        pago.id_estudiante_id = request.POST.get('id_estudiante')
        pago.concepto = request.POST.get('concepto')
        pago.monto = request.POST.get('monto')
        pago.fecha_pago = request.POST.get('fecha_pago') or None
        pago.metodo_pago = request.POST.get('metodo_pago')
        pago.estado = request.POST.get('estado')
        pago.save()
        
        messages.success(request, 'Pago actualizado correctamente')
        return redirect('pago_list')
    
    estudiantes = Estudiante.objects.all()
    context = {'pago': pago, 'estudiantes': estudiantes}
    return render(request, 'payments/pago_form.html', context)


@requerido_login
@estudiante_no_editable
def pago_delete(request, pk):
    """Elimina un pago"""
    pago = get_object_or_404(Pago, pk=pk)
    
    if request.method == 'POST':
        pago.delete()
        messages.success(request, 'Pago eliminado correctamente')
        return redirect('pago_list')
    
    context = {'pago': pago}
    return render(request, 'payments/pago_confirm_delete.html', context)


@requerido_login
@estudiante_no_editable
def pago_registrar(request, pk):
    """Registra el pago de una deuda"""
    pago = get_object_or_404(Pago, pk=pk)
    
    if request.method == 'POST':
        pago.fecha_pago = request.POST.get('fecha_pago')
        pago.metodo_pago = request.POST.get('metodo_pago')
        pago.estado = 'pagado'
        pago.save()

        messages.success(request, 'Pago registrado correctamente')
        return redirect('pago_list')

    context = {'pago': pago}
    # Reutilizamos el formulario de edición para evitar la falta de template específico.
    return render(request, 'payments/pago_form.html', context)

