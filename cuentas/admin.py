from django.contrib import admin
from .models import CuentaUsuario


@admin.register(CuentaUsuario)
class CuentaUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "rol", "activo", "creado_el")
    list_filter = ("rol", "activo")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name")
