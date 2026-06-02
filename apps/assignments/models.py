from django.db import models
from django.db import models


class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_entrega = models.DateField()
    id_materia = models.ForeignKey(
        'academic.Materia',
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    id_profesor = models.ForeignKey(
        'people.Profesor',
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-created_at']

    def __str__(self):
        return self.titulo
# Create your models here.
