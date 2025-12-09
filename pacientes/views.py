from django.shortcuts import render, redirect
from .models import Paciente
from .forms import PacienteForm
from django.contrib.auth.decorators import login_required


@login_required  
def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by("-fecha_registro")
    context = {"pacientes": pacientes}
    return render(request, "pacientes/lista_pacientes.html", context)



def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by("-fecha_registro")
    context = {"pacientes": pacientes}
    return render(request, "pacientes/lista_pacientes.html", context)


def crear_paciente(request):
    if request.method == "POST":
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_pacientes")
    else:
        form = PacienteForm()

    context = {"form": form}
    return render(request, "pacientes/formulario_pacientes.html", context)
