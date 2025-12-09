from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from pacientes.models import Paciente

class Procedimiento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    duracion_estimada_minutos = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class PlanTratamiento(models.Model):
    ESTADO_CHOICES = [
        ('PLAN', 'Planificado'),
        ('PROC', 'En proceso'),
        ('COMPL', 'Completado'),
        ('CANC', 'Cancelado'),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='planes_tratamiento'
    )
    fecha_creacion = models.DateField(auto_now_add=True)
    descripcion_general = models.TextField(blank=True)
    estado = models.CharField(max_length=5, choices=ESTADO_CHOICES, default='PLAN')

    def __str__(self):
        return f"Plan {self.id} - {self.paciente}"

    
    @property
    def total_estimado(self):
    
        detalles = self.detalles.all()
        if not detalles:
            return Decimal('0.00')
        return sum(d.subtotal for d in detalles)


class DetallePlan(models.Model):
    plan = models.ForeignKey(
        PlanTratamiento,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    procedimiento = models.ForeignKey(Procedimiento, on_delete=models.PROTECT)
    pieza_dental = models.CharField(max_length=10, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    descuento_porcentaje = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[
            MinValueValidator(Decimal('0.00')),
            MaxValueValidator(Decimal('100.00'))
        ]
    )
    
    completado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.precio_unitario is None:
            self.precio_unitario = self.procedimiento.precio_base
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.procedimiento} x{self.cantidad}"

    @property
    def subtotal(self):
        if not self.precio_unitario:
            return Decimal('0.00')
        
        factor_descuento = Decimal(1) - (self.descuento_porcentaje / Decimal(100))
        total = (self.cantidad * self.precio_unitario) * factor_descuento
        return total.quantize(Decimal('0.01'))