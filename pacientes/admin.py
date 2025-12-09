from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'telefono', 'email', 'activo', 'fecha_registro')
    search_fields = ('nombre', 'apellidos', 'telefono', 'email')
    list_filter = ('activo', 'sexo')