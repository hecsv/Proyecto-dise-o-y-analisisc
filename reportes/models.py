from django.db import models
from django.db.models import F
from pacientes.models import Paciente
from tratamientos.models import PlanTratamiento
from inventario.models import Producto


class ReporteMensual(models.Model):
    fecha_reporte = models.DateField(
        help_text="Selecciona cualquier día del mes que quieres analizar"
    )
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    
    
    total_pacientes = models.PositiveIntegerField(default=0, editable=False)
    pacientes_nuevos_mes = models.PositiveIntegerField(default=0, editable=False)
    
    
    tratamientos_iniciados = models.PositiveIntegerField(default=0, editable=False)
    tratamientos_completados = models.PositiveIntegerField(default=0, editable=False)
    
    
    productos_bajo_stock = models.PositiveIntegerField(default=0, editable=False)
    
    
    observaciones = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        year = self.fecha_reporte.year
        month = self.fecha_reporte.month

        
        self.total_pacientes = Paciente.objects.count()
        self.pacientes_nuevos_mes = Paciente.objects.filter(
            fecha_registro__year=year,
            fecha_registro__month=month
        ).count()

        
        self.tratamientos_iniciados = PlanTratamiento.objects.filter(
            fecha_creacion__year=year,
            fecha_creacion__month=month
        ).count()

        self.tratamientos_completados = PlanTratamiento.objects.filter(
            estado='COMPL',
            fecha_creacion__year=year,
            fecha_creacion__month=month
        ).count()

    
        self.productos_bajo_stock = Producto.objects.filter(
            stock__lte=F('stock_minimo')
        ).count()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reporte {self.fecha_reporte.strftime('%B %Y')}"

    class Meta:
        verbose_name = "Reporte Mensual"
        verbose_name_plural = "Reportes Mensuales"
