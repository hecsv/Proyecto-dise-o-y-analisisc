from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, registro_publico, crear_cita_paciente, historial_clinico
from citas.views import lista_citas, crear_cita  
from pacientes.views import lista_pacientes, crear_paciente
from facturacion.views import lista_pagos, crear_pago, lista_facturas, crear_factura
from inventario.views import (
    lista_productos, crear_producto, 
    lista_proveedores, crear_proveedor, 
    lista_categorias, crear_categoria, 
    lista_movimientos, crear_movimiento
)
from reportes.views import lista_reportes, crear_reporte, detalle_reporte
from cuentas.views import registrar_cuenta, mi_perfil


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', registro_publico, name='registro_paciente'),
    path('agendar-cita/', crear_cita_paciente, name='crear_cita_paciente'),
    path('mi-historial/', historial_clinico, name='historial_clinico'),
    path('citas/', lista_citas, name='lista_citas'),
    path('citas/nueva/', crear_cita, name='crear_cita'),
    path("pacientes/", lista_pacientes, name="lista_pacientes"),
    path("pacientes/nuevo/", crear_paciente, name="crear_paciente"),
    path("pagos/", lista_pagos, name="lista_pagos"),
    path("pagos/nuevo/", crear_pago, name="crear_pago"),
    path("facturas/", lista_facturas, name="lista_facturas"),
    path("facturas/nueva/", crear_factura, name="crear_factura"),
    path("inventario/productos/", lista_productos, name="lista_productos"),
    path("inventario/productos/nuevo/", crear_producto, name="crear_producto"),
    path("inventario/proveedores/", lista_proveedores, name="lista_proveedores"),
    path("inventario/proveedores/nuevo/", crear_proveedor, name="crear_proveedor"),
    path("inventario/categorias/", lista_categorias, name="lista_categorias"),
    path("inventario/categorias/nueva/", crear_categoria, name="crear_categoria"),
    path("inventario/movimientos/", lista_movimientos, name="lista_movimientos"),
    path("inventario/movimientos/nuevo/", crear_movimiento, name="crear_movimiento"),
    path("reportes/", lista_reportes, name="lista_reportes"),
    path("reportes/nuevo/", crear_reporte, name="crear_reporte"),
    path("reportes/<int:pk>/", detalle_reporte, name="detalle_reporte"),
    path("cuentas/nueva/", registrar_cuenta, name="registrar_cuenta"),
    path("mi-perfil/", mi_perfil, name="mi_perfil"),
]