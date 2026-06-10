from django.contrib import admin
from .models import Grado, Materia


@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    list_display = ['nombre_grado', 'nivel', 'jornada']
    list_filter = ['nivel', 'jornada']
    search_fields = ['nombre_grado']


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['nombre_materia', 'id_grado', 'id_profesor', 'intensidad_horaria']
    list_filter = ['id_grado']
    search_fields = ['nombre_materia']
    raw_id_fields = ['id_grado', 'id_profesor']