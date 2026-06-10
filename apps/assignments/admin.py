from django.contrib import admin
from .models import Tarea


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'id_materia', 'id_profesor', 'fecha_entrega', 'created_at']
    list_filter = ['id_materia', 'id_profesor']
    search_fields = ['titulo', 'descripcion']
    raw_id_fields = ['id_materia', 'id_profesor']
    readonly_fields = ['created_at']