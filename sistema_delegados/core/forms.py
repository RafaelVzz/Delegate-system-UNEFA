from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Seccion

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=150, required=True)
    last_name = forms.CharField(label="Apellido", max_length=150, required=True)
    email = forms.EmailField(required=True, label="Correo Electrónico")
    seccion_base = forms.ModelChoiceField(queryset=Seccion.objects.all(), required=True, label="Sección Base")
    cedula = forms.IntegerField(required=True, label="Cédula")

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('cedula', 'first_name', 'last_name', 'email', 'seccion_base')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = str(self.cleaned_data['cedula'])
        if commit:
            user.save()
        return user

