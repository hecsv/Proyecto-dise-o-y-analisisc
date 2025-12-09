from django.urls import path
from . import views

urlpatterns = [
    
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),

    
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/nuevo/', views.crear_proveedor, name='crear_proveedor'),

    
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),

    
    path('movimientos/', views.lista_movimientos, name='lista_movimientos'),
    path('movimientos/nuevo/', views.crear_movimiento, name='crear_movimiento'),
]