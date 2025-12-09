from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    activo = models.BooleanField(default=True)

   
    class Meta:
        verbose_name_plural = "Proveedores"

    
    def __str__(self):
        return self.nombre


class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

class Meta:
    verbose_name = "Categoría de Producto"
    verbose_name_plural = "Categorías de Productos"


    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    
    categoria = models.ForeignKey(
        CategoriaProducto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    
    stock = models.IntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    
    
    precio_compra = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    precio_venta = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    
    cantidad = models.PositiveIntegerField() 
    motivo = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"

    
    def __str__(self):
        return f"{self.tipo} {self.cantidad} de {self.producto}"