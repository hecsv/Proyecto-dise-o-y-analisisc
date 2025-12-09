from django import forms
from .models import Pago, Factura


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ["paciente", "cita", "monto", "metodo", "referencia", "notas"]

        widgets = {
            "paciente": forms.Select(attrs={"class": "form-select"}),
            "cita": forms.Select(attrs={"class": "form-select"}),

            "monto": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "metodo": forms.Select(attrs={"class": "form-select"}),

            "referencia": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Folio, referencia bancaria, etc."
                }
            ),

            "notas": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Notas adicionales (opcional)"
                }
            ),
        }


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [
            "paciente",
            "pago",
            "serie",
            "folio",
            "subtotal",
            "impuestos",
            "total",
            "estatus",
        ]

    widgets = {
        "paciente": forms.Select(attrs={"class": "form-select"}),
        "pago": forms.Select(attrs={"class": "form-select"}),

        "serie": forms.TextInput(attrs={"class": "form-control"}),
        "folio": forms.TextInput(attrs={"class": "form-control"}),

        "subtotal": forms.NumberInput(
            attrs={"class": "form-control", "step": "0.01", "min": "0"}
        ),
        "impuestos": forms.NumberInput(
            attrs={"class": "form-control", "step": "0.01", "min": "0"}
        ),
        "total": forms.NumberInput(
            attrs={"class": "form-control", "step": "0.01", "min": "0"}
        ),

        "estatus": forms.Select(attrs={"class": "form-select"}),
    }
