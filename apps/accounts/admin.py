from django.contrib import admin
from .models import Rol, Usuario


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre_rol', 'descripcion']
    search_fields = ['nombre_rol']


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'telefono', 'estado', 'id_rol', 'fecha_registro']
    list_filter = ['estado', 'id_rol']
    search_fields = ['username', 'telefono']
    list_editable = ['estado']
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('username', 'password', 'telefono')
        }),
        ('Estado y Rol', {
            'fields': ('estado', 'id_rol')
        }),
    )