from django.contrib import admin
from .models import Estudiante, Profesor


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['codigo_estudiante', 'nombre', 'apellido', 'id_grado', 'correo']
    list_filter = ['id_grado']
    search_fields = ['codigo_estudiante', 'nombre', 'apellido', 'correo']
    raw_id_fields = ['id_usuario', 'id_grado']


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'especialidad', 'correo']
    list_filter = ['especialidad']
    search_fields = ['nombre', 'apellido', 'correo']
    raw_id_fields = ['id_usuario']