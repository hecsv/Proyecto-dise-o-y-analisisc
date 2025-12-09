from django.contrib import admin
from .models import ReporteMensual

@admin.register(ReporteMensual)
class ReporteMensualAdmin(admin.ModelAdmin):
    
    list_display = (
        '__str__', 
        'fecha_generacion', 
        'pacientes_nuevos_mes', 
        'tratamientos_completados', 
        'alerta_inventario'
    )
    

    readonly_fields = (
        'fecha_generacion',
        'total_pacientes',
        'pacientes_nuevos_mes',
        'tratamientos_iniciados',
        'tratamientos_completados',
        'productos_bajo_stock'
    )

    fieldsets = (
        ('Configuración', {
            'fields': ('fecha_reporte', 'observaciones')
        }),
        ('Estadísticas de Pacientes', {
            'fields': ('total_pacientes', 'pacientes_nuevos_mes')
        }),
        ('Estadísticas de Tratamientos', {
            'fields': ('tratamientos_iniciados', 'tratamientos_completados')
        }),
        ('Estadísticas de Inventario', {
            'fields': ('productos_bajo_stock',)
        }),
    )


    def alerta_inventario(self, obj):
        if obj.productos_bajo_stock > 0:
            return f"⚠️ {obj.productos_bajo_stock} productos bajos"
        return " Todo bien"
    alerta_inventario.short_description = "Estado Inventario"