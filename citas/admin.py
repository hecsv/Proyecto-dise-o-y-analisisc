from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora_inicio', 'hora_fin', 'paciente', 'odontologo', 'estado', 'sala')
    list_filter = ('estado', 'fecha', 'odontologo')
    

    search_fields = (
        'paciente__nombre',
        'paciente__apellidos', 
        'motivo',
    )
    
    
    autocomplete_fields = ['paciente', 'odontologo']


    exclude = ('creado_por',)

    
    def save_model(self, request, obj, form, change):
        if not obj.pk: 
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)