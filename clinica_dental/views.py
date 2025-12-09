from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import F
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django import forms
import datetime

from citas.models import Cita
from pacientes.models import Paciente
from inventario.models import Producto
from tratamientos.models import PlanTratamiento
from .forms import RegistroPacienteForm


class CitaPacienteForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora_inicio', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Dolor de muela, Limpieza...'}),
        }
        labels = {
            'hora_inicio': 'Hora deseada'
        }


@login_required
def home(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    hoy = timezone.now().date()
    usuario = request.user
    rol = None

    if hasattr(usuario, 'cuenta'):
        rol = usuario.cuenta.rol
    elif hasattr(usuario, 'paciente'):
        rol = 'PACIENTE'

    if rol == 'PACIENTE':
        try:
            paciente_ficha = usuario.paciente
            mis_citas = Cita.objects.filter(
                paciente=paciente_ficha,
                fecha__gte=hoy
            ).order_by('fecha', 'hora_inicio')
        except Paciente.DoesNotExist:
            mis_citas = []

        context = {
            'rol_usuario': 'PACIENTE',
            'mis_citas': mis_citas,
            'fecha_hoy': hoy,
            'nombre_paciente': usuario.first_name
        }
        return render(request, 'home.html', context)

    elif rol == 'ODONTO':
        citas_hoy = Cita.objects.filter(fecha=hoy, odontologo=usuario).count()
        proximas_citas = Cita.objects.filter(
            fecha=hoy,
            estado='pendiente',
            odontologo=usuario
        ).order_by('hora_inicio')[:5]
    else:
        citas_hoy = Cita.objects.filter(fecha=hoy).count()
        proximas_citas = Cita.objects.filter(
            fecha=hoy,
            estado='pendiente'
        ).order_by('hora_inicio')[:5]

    total_pacientes = Paciente.objects.count()
    productos_alerta = Producto.objects.filter(stock__lte=F('stock_minimo')).count()

    context = {
        'fecha_hoy': hoy,
        'citas_hoy': citas_hoy,
        'total_pacientes': total_pacientes,
        'productos_alerta': productos_alerta,
        'proximas_citas': proximas_citas,
        'rol_usuario': rol,
    }
    return render(request, 'home.html', context)


def registro_publico(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroPacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            login(request, paciente.usuario)
            return redirect('home')
    else:
        form = RegistroPacienteForm()

    return render(request, 'registro.html', {'form': form})


@login_required
def crear_cita_paciente(request):
    if not hasattr(request.user, 'paciente'):
        return redirect('home')

    if request.method == 'POST':
        form = CitaPacienteForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = request.user.paciente

            hoy = timezone.localdate()
            if cita.fecha < hoy:
                form.add_error('fecha', 'No se pueden agendar citas en fechas pasadas.')
            else:
                hora_min = datetime.time(9, 0)
                hora_max = datetime.time(19, 0)
                if not (hora_min <= cita.hora_inicio <= hora_max):
                    form.add_error('hora_inicio', 'La hora debe estar entre 09:00 y 19:00.')
                else:
                    User = get_user_model()
                    doctor = User.objects.filter(cuenta__rol='ODONTO', is_active=True).first()
                    if doctor is None:
                        doctor = User.objects.filter(is_superuser=True).first()
                    cita.odontologo = doctor

                    dummy_date = datetime.datetime.combine(cita.fecha, cita.hora_inicio)
                    cita.hora_fin = (dummy_date + datetime.timedelta(minutes=30)).time()
                    cita.estado = 'pendiente'

                    conflictos = Cita.objects.filter(
                        odontologo=cita.odontologo,
                        fecha=cita.fecha,
                        hora_inicio__lt=cita.hora_fin,
                        hora_fin__gt=cita.hora_inicio,
                    )
                    if conflictos.exists():
                        form.add_error(None, 'El odontólogo ya tiene una cita en ese horario.')
                    else:
                        cita.save()
                        return redirect('home')
    else:
        form = CitaPacienteForm()

    return render(request, 'citas/crear_cita_paciente.html', {'form': form})


@login_required
def historial_clinico(request):
    if not hasattr(request.user, 'paciente'):
        return redirect('home')

    paciente = request.user.paciente

    citas_pasadas = Cita.objects.filter(
        paciente=paciente,
        fecha__lt=timezone.now().date()
    ).order_by('-fecha')

    tratamientos = PlanTratamiento.objects.filter(
        paciente=paciente
    ).order_by('-fecha_creacion')

    context = {
        'citas_pasadas': citas_pasadas,
        'tratamientos': tratamientos
    }
    return render(request, 'pacientes/historial_clinico.html', context)
