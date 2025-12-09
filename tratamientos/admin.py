from django.contrib import admin
from .models import Procedimiento, PlanTratamiento, DetallePlan

class DetallePlanInline(admin.TabularInline):
    model = DetallePlan
    extra = 0  
    autocomplete_fields = ['procedimiento'] 
    readonly_fields = ('subtotal_ver',) 

    def subtotal_ver(self, obj):
        return obj.subtotal
    subtotal_ver.short_description = "Subtotal"


@admin.register(PlanTratamiento)
class PlanTratamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'fecha_creacion', 'estado', 'ver_total')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('paciente__nombre', 'paciente__apellidos')
    autocomplete_fields = ['paciente'] 
    inlines = [DetallePlanInline]

    
    def ver_total(self, obj):
        return f"${obj.total_estimado}"
    ver_total.short_description = "Total Estimado"


@admin.register(Procedimiento)
class ProcedimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_base', 'duracion_estimada_minutos')
    search_fields = ('nombre',)