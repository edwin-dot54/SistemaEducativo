from django.contrib import admin
from .models import Horario


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['id_grado', 'id_materia', 'dia_semana', 'hora_inicio', 'hora_fin', 'aula']
    list_filter = ['id_grado', 'dia_semana']
    search_fields = ['id_grado__nombre_grado', 'id_materia__nombre_materia']
    raw_id_fields = ['id_grado', 'id_materia']
    ordering = ['id_grado', 'dia_semana', 'hora_inicio']