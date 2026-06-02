from django.db import models
from django.db import models


class Horario(models.Model):
    DIA_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado')
    ]

    id_grado = models.ForeignKey(
        'academic.Grado',
        on_delete=models.CASCADE,
        related_name='horarios'
    )
    id_materia = models.ForeignKey(
        'academic.Materia',
        on_delete=models.CASCADE,
        related_name='horarios'
    )
    dia_semana = models.CharField(max_length=20, choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    aula = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        unique_together = ['id_grado', 'dia_semana', 'hora_inicio']

    def __str__(self):
        return f"{self.id_grado} - {self.get_dia_semana_display()} {self.hora_inicio}"
# Create your models here.
