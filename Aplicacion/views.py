from django.shortcuts import render

def mostrarHome(request):
    return render(request, 'html/home.html')

def mostrarComunidad(request):
    return render(request, 'html/comunidad.html')


def mostrarRutas(request):
    return render(request, 'html/rutas.html')

def mostrarJuegos(request):
    return render(request, 'html/juegos/juegos.html')

def mostrarRanking(request):
    return render(request, 'html/ranking.html')
# Create your views here.

# creacion de las vistas para el formulario de registro de datos para los usuarios

# Aplicacion/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User # Importa el modelo User de Django
# Si creaste un Profile, impórtalo también:
# from .models import Profile

def registro(request):
    if request.method == 'POST':
        # Crea una instancia del formulario de creación de usuario de Django
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Guarda el nuevo usuario en la base de datos
            user = form.save()
            # Si tienes un perfil adicional, puedes crearlo aquí:
            # Profile.objects.create(user=user, full_name=request.POST.get('usuario')) # Asumiendo que 'usuario' es el nombre completo
            login(request, user) # Inicia sesión al usuario automáticamente después del registro
            return redirect('nombre_de_tu_pagina_de_inicio') # Redirige a una página de éxito o inicio
        else:
            # Si el formulario no es válido, puedes pasar los errores al template
            return render(request, 'registro.html', {'form': form})
    else:
        form = UserCreationForm() # Crea un formulario vacío para GET requests
    return render(request, 'registro.html', {'form': form})

def login_view(request):
    # Aquí iría tu lógica para el login
    return render(request, 'login.html')