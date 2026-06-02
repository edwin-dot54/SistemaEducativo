from django.db import models
from django.db import models


class Asistencia(models.Model):
    ESTADO_CHOICES = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('tarde', 'Tarde'),
        ('justificado', 'Justificado')
    ]

    id_estudiante = models.ForeignKey(
        'people.Estudiante',
        on_delete=models.CASCADE,
        related_name='asistencias'
    )
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    observacion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        unique_together = ['id_estudiante', 'fecha']
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.id_estudiante} - {self.fecha}: {self.get_estado_display()}"
# Create your models here.
