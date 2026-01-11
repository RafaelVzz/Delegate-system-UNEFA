from django.shortcuts import render, redirect
from django.contrib.auth import login #login directo después del registro válido
from .forms import RegistroForm #Formulario de registro proveniente del archivo forms.py

#Función que maneja el registro de usuarios
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST) #Creación de un objeto tipo RegistroForm
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

#Este archivo se va a conectar con core/registro.html
