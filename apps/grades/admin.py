from django.contrib import admin
from .models import Nota


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ['id_estudiante', 'id_materia', 'periodo', 'nota', 'fecha_registro']
    list_filter = ['periodo', 'id_materia']
    search_fields = ['id_estudiante__nombre', 'id_estudiante__apellido']
    raw_id_fields = ['id_estudiante', 'id_materia']
    ordering = ['-fecha_registro']