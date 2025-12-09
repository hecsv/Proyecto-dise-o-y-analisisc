from django import forms
from django.contrib.auth.models import User, Group
from pacientes.models import Paciente

class RegistroPacienteForm(forms.ModelForm):

    username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
  
    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(label="Apellidos", widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label="Teléfono", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Paciente
        fields = ['nombre', 'apellidos', 'telefono']

    def save(self, commit=True):
        
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['nombre'],
            last_name=self.cleaned_data['apellidos']
        )
        
        

      
        paciente = super().save(commit=False)
        paciente.usuario = user
        if commit:
            paciente.save()
        return paciente