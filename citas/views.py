from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Cita
from .forms import CitaForm

def lista_citas(request):
    citas = Cita.objects.all().order_by('fecha', 'hora_inicio')
    return render(request, 'citas/citas_lista.html', {'citas': citas})

def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)

            User = get_user_model()
            doctor_disponible = User.objects.filter(cuenta__rol='ODONTO').first()
            if not doctor_disponible:
                doctor_disponible = User.objects.filter(is_superuser=True).first()
            
            cita.odontologo = doctor_disponible

            if request.user.is_authenticated:
                cita.creado_por = request.user
            
            cita.save()
            messages.success(request, '¡Cita agendada correctamente!')
            return redirect('lista_citas')
        else:
            messages.error(request, 'Hubo un error. Revisa las horas.')
    else:
        form = CitaForm()
    
    return render(request, 'citas/citas_form.html', {'form': form})

@login_required
def actualizar_estado_cita(request, cita_id, nuevo_estado):
    if not request.user.is_staff:
        return redirect('home')
        
    cita = get_object_or_404(Cita, pk=cita_id)
    
    if nuevo_estado in ['confirmada', 'cancelada', 'atendida', 'pendiente', 'no_asistio']:
        cita.estado = nuevo_estado
        cita.save()
        messages.success(request, f'Cita de {cita.paciente} actualizada a {cita.get_estado_display()}')
    else:
        messages.error(request, 'Estado no válido.')
        
    return redirect('lista_citas')