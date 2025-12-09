from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import CuentaUsuario

User = get_user_model()


class RegistroUsuarioForm(UserCreationForm):
    
    first_name = forms.CharField(label="Nombre", max_length=150, required=False)
    last_name = forms.CharField(label="Apellidos", max_length=150, required=False)
    email = forms.EmailField(label="Correo electrónico", required=False)

    
    rol = forms.ChoiceField(
        label="Rol en la clínica",
        choices=CuentaUsuario.Rol.choices,
    )
    telefono = forms.CharField(label="Teléfono", max_length=20, required=False)
    notas = forms.CharField(
        label="Notas",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        
        user = super().save(commit=commit)

        
        if commit:
            CuentaUsuario.objects.create(
                usuario=user,
                rol=self.cleaned_data["rol"],
                telefono=self.cleaned_data.get("telefono", ""),
                notas=self.cleaned_data.get("notas", ""),
            )

        return user
