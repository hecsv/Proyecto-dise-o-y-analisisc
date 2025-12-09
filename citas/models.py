from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from pacientes.models import Paciente

User = get_user_model()

class Cita(models.Model):

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"
        ATENDIDA = "atendida", "Atendida"
        NO_ASISTIO = "no_asistio", "No asistió"

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name='citas'
    )
    odontologo = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='citas_odontologo',
        help_text="Usuario con rol de odontólogo"
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    
    motivo = models.CharField(max_length=255, blank=True)
    sala = models.CharField(max_length=50, blank=True)
    
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    observaciones = models.TextField(blank=True)

    
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='citas_creadas',
        null=True,   
        blank=True
    )
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha', 'hora_inicio']
        
        unique_together = ('odontologo', 'fecha', 'hora_inicio')

    def clean(self):
        
        if self.hora_inicio and self.hora_fin:
            if self.hora_fin <= self.hora_inicio:
                raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")

    def __str__(self):
        return f"{self.fecha} {self.hora_inicio} - {self.paciente}"