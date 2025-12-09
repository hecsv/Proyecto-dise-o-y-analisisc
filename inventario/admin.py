from django.contrib import admin
from .models import Proveedor, CategoriaProducto, Producto, MovimientoInventario

@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'activo')
    search_fields = ('nombre', 'telefono', 'email')
    list_filter = ('activo',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'categoria', 'stock', 'precio_venta', 'activo')
    search_fields = ('nombre', 'codigo')
    list_filter = ('categoria', 'activo')
    
    autocomplete_fields = ['categoria', 'proveedor']


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'fecha', 'motivo')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre', 'producto__codigo')
    autocomplete_fields = ['producto']