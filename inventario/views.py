from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Producto, Proveedor, CategoriaProducto, MovimientoInventario
from .forms import (
    ProductoForm,
    ProveedorForm,
    CategoriaProductoForm,
    MovimientoInventarioForm,
)



def es_admin(user):
    return user.is_authenticated and user.is_staff




@user_passes_test(es_admin)
def lista_productos(request):
    productos = Producto.objects.select_related("categoria", "proveedor").order_by("nombre")
    return render(request, "inventario/productos_lista.html", {"productos": productos})


@user_passes_test(es_admin)
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form = ProductoForm()

    return render(request, "inventario/productos_formulario.html", {"form": form})




@user_passes_test(es_admin)
def lista_proveedores(request):
    proveedores = Proveedor.objects.all().order_by("nombre")
    return render(request, "inventario/proveedores_lista.html", {"proveedores": proveedores})


@user_passes_test(es_admin)
def crear_proveedor(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_proveedores")
    else:
        form = ProveedorForm()

    return render(request, "inventario/proveedores_formulario.html", {"form": form})




@user_passes_test(es_admin)
def lista_categorias(request):
    categorias = CategoriaProducto.objects.all().order_by("nombre")
    return render(request, "inventario/categorias_lista.html", {"categorias": categorias})


@user_passes_test(es_admin)
def crear_categoria(request):
    if request.method == "POST":
        form = CategoriaProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_categorias")
    else:
        form = CategoriaProductoForm()

    return render(request, "inventario/categorias_formulario.html", {"form": form})




@user_passes_test(es_admin)
def lista_movimientos(request):
    movimientos = MovimientoInventario.objects.select_related("producto").order_by("-fecha")
    return render(request, "inventario/movimientos_lista.html", {"movimientos": movimientos})


@user_passes_test(es_admin)
def crear_movimiento(request):
    if request.method == "POST":
        form = MovimientoInventarioForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)

            producto = movimiento.producto
            cantidad = movimiento.cantidad
            tipo = movimiento.tipo 

            
            if tipo == "ENTRADA":
                producto.stock += cantidad
            elif tipo == "SALIDA":
                producto.stock -= cantidad
                if producto.stock < 0:
                    producto.stock = 0
            elif tipo == "AJUSTE":
                producto.stock = cantidad

            producto.save()
            movimiento.save()

            return redirect("lista_movimientos")
    else:
        form = MovimientoInventarioForm()

    return render(request, "inventario/movimientos_formulario.html", {"form": form})
