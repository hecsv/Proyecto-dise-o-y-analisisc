from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}".strip()