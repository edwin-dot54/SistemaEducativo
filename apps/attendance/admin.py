from django.contrib import admin
from .models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['id_estudiante', 'fecha', 'estado', 'observacion']
    list_filter = ['estado', 'fecha']
    search_fields = ['id_estudiante__nombre', 'id_estudiante__apellido']
    raw_id_fields = ['id_estudiante']
    ordering = ['-fecha']