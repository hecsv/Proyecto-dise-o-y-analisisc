from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import RegistroUsuarioForm
from .models import CuentaUsuario


def es_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(es_admin)
def registrar_cuenta(request):
    """
    Vista para que el ADMIN cree cuentas de usuarios (odontólogos, recepción, etc.)
    """
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = RegistroUsuarioForm()

    return render(request, "cuentas/registro_cuenta.html", {"form": form})


@login_required
def mi_perfil(request):
    """
    Vista para que cada usuario vea su perfil/cuenta.
    """
    cuenta = getattr(request.user, "cuenta", None)
    return render(request, "cuentas/mi_perfil.html", {"cuenta": cuenta})
