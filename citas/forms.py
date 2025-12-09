from django import forms
from .models import Cita


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        
        exclude = ["creado_por", "creado_el", "actualizado_el", "sala", "odontologo"]

        widgets = {
            "paciente": forms.Select(attrs={"class": "form-select"}),
           
            "fecha": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "hora_inicio": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "hora_fin": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),

            "motivo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Motivo de la consulta"}
            ),
            "sala": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej. Sala 1"}
            ),

            "estado": forms.Select(attrs={"class": "form-select"}),

            "observaciones": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Notas adicionales"}
            ),
        }