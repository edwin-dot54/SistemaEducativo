from django.db import models
from django.db import models
from django.conf import settings


class Estudiante(models.Model):
    codigo_estudiante = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(max_length=100)
    id_usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='estudiante',
        null=True,
        blank=True
    )
    id_grado = models.ForeignKey(
        'academic.Grado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='estudiantes'
    )

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['apellido', 'nombre']

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return f"{self.codigo_estudiante} - {self.nombre_completo}"


class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(max_length=100)
    id_usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profesor',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['apellido', 'nombre']

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return self.nombre_completo
# Create your models here.
