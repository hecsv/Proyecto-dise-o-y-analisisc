from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import ReporteMensual
from .forms import ReporteMensualForm



def es_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(es_admin)
def lista_reportes(request):
    reportes = ReporteMensual.objects.order_by("-fecha_reporte")
    return render(request, "reportes/lista_reportes.html", {"reportes": reportes})


@user_passes_test(es_admin)
def crear_reporte(request):
    if request.method == "POST":
        form = ReporteMensualForm(request.POST)
        if form.is_valid():
            reporte = form.save()
            
            return redirect("detalle_reporte", pk=reporte.pk)
    else:
        form = ReporteMensualForm()

    return render(request, "reportes/formulario_reportes.html", {"form": form})


@user_passes_test(es_admin)
def detalle_reporte(request, pk):
    reporte = get_object_or_404(ReporteMensual, pk=pk)
    return render(request, "reportes/detalles_reportes.html", {"reporte": reporte})
