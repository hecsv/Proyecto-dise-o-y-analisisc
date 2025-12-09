from django import forms
from .models import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nombre",
            "apellidos",
            "fecha_nacimiento",
            "sexo",
            "telefono",
            "email",
            "direccion",
            "activo",
        ]

        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellidos": forms.TextInput(attrs={"class": "form-control"}),

            "fecha_nacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),

            "sexo": forms.Select(attrs={"class": "form-select"}),

            "telefono": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej. 555-123-4567"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Calle, número, colonia"}
            ),

            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
