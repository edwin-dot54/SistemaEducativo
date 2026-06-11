from django.contrib import admin
from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id_estudiante', 'concepto', 'monto', 'estado', 'fecha_pago']
    list_filter = ['estado', 'concepto', 'metodo_pago']
    search_fields = ['id_estudiante__nombre', 'id_estudiante__apellido']
    raw_id_fields = ['id_estudiante']
    ordering = ['-id']