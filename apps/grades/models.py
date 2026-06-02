from django.db import models
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Nota(models.Model):
    PERIODO_CHOICES = [
        ('1', 'Primer Período'),
        ('2', 'Segundo Período'),
        ('3', 'Tercer Período'),
        ('4', 'Cuarto Período')
    ]

    id_estudiante = models.ForeignKey(
        'people.Estudiante',
        on_delete=models.CASCADE,
        related_name='notas'
    )
    id_materia = models.ForeignKey(
        'academic.Materia',
        on_delete=models.CASCADE,
        related_name='notas'
    )
    periodo = models.CharField(max_length=20, choices=PERIODO_CHOICES)
    nota = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    observacion = models.TextField(blank=True)
    fecha_registro = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ['id_estudiante', 'id_materia', 'periodo']

    def __str__(self):
        return f"{self.id_estudiante} - {self.id_materia}: {self.nota}"
# Create your models here.
