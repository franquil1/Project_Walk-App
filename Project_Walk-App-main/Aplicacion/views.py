from django.shortcuts import render, redirect
from django.shortcuts import render,  get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroUsuarioForms, LoginForm
from .models import Ruta
from .forms import RutaForm 
from django.contrib.auth.decorators import login_required 
from .models import Ruta, Usuario, UserRutaFavorita



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
    return render(request, 'html/juegos/trivia/index.html', {
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

def vista_morro(request):
    return render(request, 'html/rutas/info/info_morro.html')

def regresar_morro(request):
    return render(request, 'html/rutas/vista-morro.html')

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

# ==== MOSTRAR RUTAS A LOS USUARIOS =====

def lista_rutas(request):
    # Obtiene todas las rutas de la base de datos
    rutas = Ruta.objects.all().order_by('nombre_ruta')
    # Pasa las rutas al contexto para que estén disponibles en la plantilla
    return render(request, 'Aplicacion/rutas.html', {'rutas': rutas})

# Vista para la lista de rutas
def lista_rutas(request):
    rutas = Ruta.objects.all().order_by('nombre_ruta')
    return render(request, 'html/rutas/rutas.html', {'rutas': rutas}) 

# Vista para los detalles de una ruta específica
def detalle_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    return render(request, 'html/rutas/detalle_ruta.html', {'ruta': ruta}) 

# Vista para crear una nueva ruta
def crear_ruta(request):
    if request.method == 'POST':
        form = RutaForm(request.POST)
        if form.is_valid():
            nueva_ruta = form.save(commit=False)
            # if request.user.is_authenticated:
            #     # Asumiendo que request.user es una instancia de Usuario (o lo mapeas)
            #     nueva_ruta.creada_por = Usuario.objects.get(nombre_usuario=request.user.username) 
            #     # O de forma más robusta:
            #     # if hasattr(request.user, 'usuario_profile'): # Si tienes un OneToOneField de User a Usuario
            #     #     nueva_ruta.creada_por = request.user.usuario_profile
            #     # else: # Si request.user es directamente tu modelo Usuario (menos común si usas el auth de Django)
            #     #     nueva_ruta.creada_por = request.user
            #     # O simplemente si siempre la va a crear un usuario existente:
            #     # nueva_ruta.creada_por = Usuario.objects.get(pk=ID_DEL_USUARIO_QUE_CREA) 
            nueva_ruta.save()
            return redirect('rutas')
    else:
        form = RutaForm()
    # Ajusta la ruta de la plantilla. Podrías crear una específica para el formulario
    return render(request, 'html/rutas/crear_ruta.html', {'form': form}) 


# Vistas para marcar/desmarcar como favorita
def marcar_favorita(request, ruta_id, usuario_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if not UserRutaFavorita.objects.filter(usuario=usuario, ruta=ruta).exists():
        UserRutaFavorita.objects.create(usuario=usuario, ruta=ruta)
    
    # Redirige de vuelta a la página de detalle de la ruta
    return redirect('detalle_ruta', ruta_id=ruta.id) 

def quitar_favorita(request, ruta_id, usuario_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    
    UserRutaFavorita.objects.filter(usuario=usuario, ruta=ruta).delete()
    
    return redirect('detalle_ruta', ruta_id=ruta.id)