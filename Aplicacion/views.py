from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegistroUsuarioForms, LoginForm, RutaForm
from .models import Ruta, Usuario, UserRutaFavorita
from .utils import account_activation_token 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

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

# VISTAS RUTAS =============================================

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
    return render(request, 'html/rutas/torre_24.html', {
        'titulo_bienvenida': 'Torre 24',
        'descripcion_bienvenida': 'RUTAS - WALK APP',
    })

# LOGIN Y CUENTA =============================================
    
        # === registro ===

@login_required
def profile_view(request):
    # Puedes pasar información del usuario al contexto si lo necesitas
    context = {
        'nombre_usuario': request.user,
        'correo_electronico': request.user.email,
        'contraseña':request.user.password,
        
    }
    return render(request, 'html/perfil.html', context)

def mostrarLogin(request):
    return render(request, 'login/index.html')

def mostrarLogin2(request):
    return render(request, 'login/mi_perfil.html')

def mostrarLogin3(request):
    return render(request, 'login/recuperar_contrasena.html')

def mostrarLogin5(request):
    return render(request, 'login/restablecer_contrasena.html')

# JUEGOS =============================================

def mostrarVideogames(request):
    return render(request, 'html/juegos/trivia/index.html')

def mostrarVideogames11(request):
    return render(request, 'html/juegos/trivia/menu.html')

def mostrarVideogames12(request):
    return render(request, 'html/juegos/trivia/juego.html')

def mostrarVideogames13(request):
    return render(request, 'html/juegos/trivia/final.html')

# REGISTRO USUARIO =============================================

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForms(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['nombre_usuario']
                email = form.cleaned_data['correo_electronico']
                password = form.cleaned_data['contraseña']

                # Crear usuario inactivo
                user_django = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user_django.is_active = False
                user_django.save()

                # Enlace de activación
                uid = urlsafe_base64_encode(force_bytes(user_django.pk))
                token = account_activation_token.make_token(user_django)
                activation_link = f"http://localhost:8000/activar/{uid}/{token}/"

                mail_subject = 'Activa tu cuenta en WalkUp'
                message = render_to_string('html/correo_activacion.html', {
                    'user': user_django,
                    'activation_link': activation_link
                })

                email_message = EmailMessage(
                    subject=mail_subject,
                    body=message,
                    to=[email]
                )
                email_message.content_subtype = "html"
                email_message.encoding = "utf-8"
                email_message.send()

                messages.success(request, 'Cuenta creada. Verifica tu correo electrónico para activarla.')
                return redirect('Aplicacion:login')

            except Exception as e:
                messages.error(request, f'Error al crear usuario: {str(e)}')
                return render(request, 'mi_app_registro/registro.html', {'form': form})
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
            return render(request, 'mi_app_registro/registro.html', {'form': form})
    else:
        form = RegistroUsuarioForms()
    return render(request, 'mi_app_registro/registro.html', {'form': form})

# ACTIVAR CUENTA =============================================

def activar_cuenta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, '¡Cuenta activada! Ya puedes iniciar sesión.')
        return redirect('login')
    else:
        messages.error(request, 'El enlace de activación no es válido.')
        return redirect('registro')

# LOGIN / LOGOUT =============================================

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

def logout_usuario(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('mi_app_registro:login')

# RUTAS (CRUD) =============================================

def lista_rutas(request):
    rutas = Ruta.objects.all().order_by('nombre_ruta')
    return render(request, 'html/rutas.html', {'rutas': rutas})

def detalle_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    return render(request, 'html/rutas/detalle_ruta.html', {'ruta': ruta})

def crear_ruta(request):
    if request.method == 'POST':
        form = RutaForm(request.POST)
        if form.is_valid():
            nueva_ruta = form.save()
            return redirect('mi_app_registro:rutas')
    else:
        form = RutaForm()
    return render(request, 'html/rutas/crear_ruta.html', {'form': form})

# FAVORITAS =============================================

def marcar_favorita(request, ruta_id, usuario_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if not UserRutaFavorita.objects.filter(usuario=usuario, ruta=ruta).exists():
        UserRutaFavorita.objects.create(usuario=usuario, ruta=ruta)

    return redirect('detalle_ruta', ruta_id=ruta.id)

def quitar_favorita(request, ruta_id, usuario_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    UserRutaFavorita.objects.filter(usuario=usuario, ruta=ruta).delete()
    return redirect('detalle_ruta', ruta_id=ruta.id)
