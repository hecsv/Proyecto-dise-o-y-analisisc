from django import forms
from .models import ReporteMensual


class ReporteMensualForm(forms.ModelForm):
    class Meta:
        model = ReporteMensual
        fields = ["fecha_reporte", "observaciones"]

        widgets = {
            "fecha_reporte": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Notas u observaciones sobre el mes..."
                }
            ),
        }

        labels = {
            "fecha_reporte": "Mes a analizar",
            "observaciones": "Observaciones",
        }
