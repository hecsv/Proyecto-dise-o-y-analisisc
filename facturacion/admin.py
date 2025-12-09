from django.contrib import admin
from .models import CuentaPaciente, MovimientoCuenta, Pago, Factura

@admin.register(CuentaPaciente)
class CuentaPacienteAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'saldo_actual', 'actualizado_el')
    search_fields = ('paciente__nombre', 'paciente__apellidos')
    autocomplete_fields = ['paciente']

    def saldo_actual(self, obj):
        return f"${obj.saldo}"


@admin.register(MovimientoCuenta)
class MovimientoCuentaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'cuenta', 'tipo', 'monto', 'concepto', 'cita')
    list_filter = ('tipo', 'fecha')
    search_fields = ('concepto', 'cuenta__paciente__nombre', 'cuenta__paciente__apellidos')
    autocomplete_fields = ['cuenta', 'cita']
    exclude = ('creado_por',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'paciente', 'monto', 'metodo', 'referencia')
    list_filter = ('metodo', 'fecha')
    search_fields = ('paciente__nombre', 'paciente__apellidos', 'referencia')
    autocomplete_fields = ['paciente', 'cita']
    exclude = ('creado_por',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'fecha_emision', 'total', 'estatus')
    list_filter = ('estatus', 'fecha_emision')
    search_fields = ('paciente__nombre', 'paciente__apellidos', 'uuid', 'folio')
    autocomplete_fields = ['paciente', 'pago']
    exclude = ('creado_por',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)