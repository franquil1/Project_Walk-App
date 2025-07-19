from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroUsuarioForms, LoginForm


# VISTAS GENERALES =============================================

def mostrarHome(request):
    return render(request, 'html/home.html')

def mostrarComunidad(request):
    return render(request, 'html/comunidad.html', {
        'titulo_bienvenida': 'COMUNIDAD ',
        'descripcion_bienvenida': 'Comparte experiencias y conecta con otros caminantes.',
    })

def mostrarRutas(request):
    return render(request, 'html/rutas.html', {
        'titulo_bienvenida': 'RUTAS',
        'descripcion_bienvenida': 'Comparte experiencias y conecta con otros caminantes.',
    })

def mostrarJuegos(request):
    return render(request, 'html/juegos/juegos.html', {
        'titulo_bienvenida': 'JUEGOS',
        'descripcion_bienvenida': 'Diviértete con nuestros juegos interactivos de senderismo.',
    })


def mostrarRanking(request):
    return render(request, 'html/ranking.html', {
        'titulo_bienvenida': 'RANKING',
        'descripcion_bienvenida': 'Celebra tus logros, escala posiciones y demuestra que cada paso vale.',
    })


# VISTAS - RUTAS    =============================================

def mostrarMorro(request):
    return render(request, 'html/rutas/vista-morro.html', {
        'titulo_bienvenida': 'El Morro',
        'descripcion_bienvenida': 'RUTAS - WALK APP',
    })

def mostrarCruces(request):
    return render(request, 'html/rutas/vista-tres-cruces.html', {
        'titulo_bienvenida': 'Las Tres Cruces',
        'descripcion_bienvenida': 'RUTAS - WALK APP',
    })

def mostrarTorre24(request):
    return render(request, 'html/rutas/torre_24.html',{
        'titulo_bienvenida':'Torre 24',
        'descripcion_bienvenida':'RUTAS - WALK APP',
    })
# ACCOUNT (CUENTA)  =============================================

# none
def mostrarLogin(request):
    return render(request, 'login/index.html')


# perfil
def mostrarLogin2(request):
    return render(request, 'login/mi_perfil.html')

# contrasena
def mostrarLogin3(request):
    return render(request, 'login/recuperar_contrasena.html')


# recuperar contraseña
def mostrarLogin5(request):
    return render(request, 'login/restablecer_contrasena.html')


# VIDEOGAMES         =============================================

# Trvia Home
def mostrarVideogames(request):
    return render(request, 'html/juegos/trivia/index.html')
# Trivia Menu
def mostrarVideogames11(request):
    return render(request, 'html/juegos/trivia/menu.html')

# Trivia Juego
def mostrarVideogames12(request):
    return render(request, 'html/juegos/trivia/juego.html')

# Trivia Final
def mostrarVideogames13(request):
    return render(request, 'html/juegos/trivia/final.html')

# funciones para registro y login

# Asegúrate de que esta función exista y esté nombrada exactamente 'registro_usuario'
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForms(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.contraseña = make_password(form.cleaned_data['contraseña'])
            usuario.save()

            try:
                user_django = User.objects.create_user(
                    username=form.cleaned_data['nombre_usuario'],
                    email=form.cleaned_data['correo_electronico'],
                    password=form.cleaned_data['contraseña']
                )
                user_django.save()
            except Exception as e:
                messages.error(request, f'Error al crear usuario de autenticación: {e}')
                print(f"Error al crear usuario de autenticación: {e}")
                return render(request, 'mi_app_registro/registro.html', {'form': form})

            messages.success(request, '¡Cuenta creada exitosamente! Por favor, inicia sesión.')
            return redirect('Aplicacion:login')
    else:
        form = RegistroUsuarioForms()

    return render(request, 'mi_app_registro/registro.html', {'form': form})

def registro_exitoso(request):
    return render(request, 'mi_app_registro/registro_exitoso.html')


def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {username}!')
                return redirect('Aplicacion:home')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'mi_app_registro/login.html', {'form': form})

def mi_pagina(request):
    if request.user.is_authenticated:
        return render(request, 'mi_app_registro/registro.html', {'username': request.user.username})
    else:
        messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
        return redirect('mi_app_registro:login')

def logout_usuario(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('mi_app_registro:login')