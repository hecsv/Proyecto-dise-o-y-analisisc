from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CuentaUsuario(models.Model):
    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        ODONTOLOGO = "ODONTO", "Odontólogo"
        RECEPCION = "RECEP", "Recepción"

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cuenta"
    )

    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.ODONTOLOGO
    )

    telefono = models.CharField(max_length=20, blank=True)
    notas = models.TextField(blank=True)

    activo = models.BooleanField(default=True)

    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.get_rol_display()})"
