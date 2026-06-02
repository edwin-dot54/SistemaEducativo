from django.db import models
from django.db import models


class Pago(models.Model):
    CONCEPTO_CHOICES = [
        ('matricula', 'Matrícula'),
        ('pension', 'Pensión'),
        ('materiales', 'Materiales'),
        ('otro', 'Otro')
    ]

    METODO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('tarjeta', 'Tarjeta')
    ]

    ESTADO_CHOICES = [
        ('pagado', 'Pagado'),
        ('pendiente', 'Pendiente'),
        ('atrasado', 'Atrasado')
    ]

    id_estudiante = models.ForeignKey(
        'people.Estudiante',
        on_delete=models.CASCADE,
        related_name='pagos'
    )
    concepto = models.CharField(max_length=100, choices=CONCEPTO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField(null=True, blank=True)
    metodo_pago = models.CharField(
        max_length=50,
        choices=METODO_CHOICES,
        blank=True
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-id']

    def __str__(self):
        return f"{self.id_estudiante} - {self.get_concepto_display()}: ${self.monto}"
# Create your models here.
