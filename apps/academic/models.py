from django.db import models
from django.db import models


class Grado(models.Model):
    NIVEL_CHOICES = [
        ('preescolar', 'Preescolar'),
        ('primaria', 'Primaria'),
        ('bachillerato', 'Bachillerato')
    ]

    JORNADA_CHOICES = [
        ('mañana', 'Mañana'),
        ('tarde', 'Tarde')
    ]

    nombre_grado = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50, choices=NIVEL_CHOICES)
    jornada = models.CharField(
        max_length=50,
        choices=JORNADA_CHOICES,
        blank=True
    )

    class Meta:
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'
        unique_together = ['nombre_grado', 'nivel', 'jornada']
        ordering = ['nivel', 'nombre_grado']

    def __str__(self):
        return f"{self.nombre_grado} ({self.get_nivel_display()})"


class Materia(models.Model):
    nombre_materia = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    intensidad_horaria = models.PositiveIntegerField(default=0)
    id_profesor = models.ForeignKey(
        'people.Profesor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='materias'
    )
    id_grado = models.ForeignKey(
        Grado,
        on_delete=models.CASCADE,
        related_name='materias'
    )

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['nombre_materia']

    def __str__(self):
        return self.nombre_materia
# Create your models here.
