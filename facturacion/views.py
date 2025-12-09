from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import FacturaForm, PagoForm
from .models import Pago, Factura


def es_admin(user):
    return user.is_authenticated and user.is_staff



@user_passes_test(es_admin)
def lista_pagos(request):
    pagos = Pago.objects.select_related("paciente", "cita").order_by("-fecha")
    return render(request, "facturacion/pagos_lista.html", {"pagos": pagos})


@user_passes_test(es_admin)
def crear_pago(request):
    if request.method == "POST":
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.creado_por = request.user
            pago.save()
            return redirect("lista_pagos")
    else:
        form = PagoForm()

    return render(request, "facturacion/pagos_formulario.html", {"form": form})




@user_passes_test(es_admin)
def lista_facturas(request):
    facturas = Factura.objects.select_related("paciente", "pago").order_by("-fecha_emision")
    return render(request, "facturacion/facturas_lista.html", {"facturas": facturas})


@user_passes_test(es_admin)
def crear_factura(request):
    if request.method == "POST":
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.creado_por = request.user
            factura.save()
            return redirect("lista_facturas")
    else:
        form = FacturaForm()

    return render(request, "facturacion/facturas_formulario.html", {"form": form})
