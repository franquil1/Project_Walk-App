# ========== IMPORTACIONES ==========
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Publicacion
from .forms import PublicacionForm, ComentarioForm

from .forms import RegistroUsuarioForms, LoginForm, RutaForm
from .models import Ruta, UsuarioPersonalizado, UserRutaFavorita, RutaRecorrida
from .utils import account_activation_token

# ========== HOME Y SECCIONES GENERALES ==========
def mostrarHome(request):
    rutas = Ruta.objects.all()
    dificultad = request.GET.get('dificultad')
    buscar = request.GET.get('buscar')
    distancia_param = request.GET.get('distancia')

    if dificultad:
        rutas = rutas.filter(dificultad__iexact=dificultad)
    if buscar:
        rutas = rutas.filter(nombre_ruta__icontains=buscar)
    if distancia_param:
        try:
            distancia = float(distancia_param)
            rutas = rutas.filter(longitud__lte=distancia)
        except ValueError:
            pass

    return render(request, 'html/home.html', {'rutas': rutas})

def mostrarComunidad(request):
    return render(request, 'html/comunidad.html')

def mostrarRutas(request):
    return render(request, 'html/rutas.html')

def mostrarJuegos(request):
    return render(request, 'html/juegos/trivia/index.html')

def mostrarRanking(request):
    return render(request, 'html/ranking.html')

# ========== VISTAS INDIVIDUALES DE RUTAS ==========
def mostrarMorro(request):
    return render(request, 'html/rutas/vista-morro.html')

def mostrarCruces(request):
    return render(request, 'html/rutas/vista-tres-cruces.html')

def mostrarTorre24(request):
    return render(request, 'html/rutas/torre_24.html')

# ========== LOGIN Y PERFIL ==========
@login_required
def profile_view(request):
    return render(request, 'html/perfil.html', {
        'nombre_usuario': request.user,
        'correo_electronico': request.user.email,
        'contraseña': request.user.password,
    })

def mostrarLogin(request):
    return render(request, 'login/index.html')

def mostrarLogin2(request):
    return render(request, 'login/mi_perfil.html')

def mostrarLogin3(request):
    return render(request, 'login/recuperar_contrasena.html')

def mostrarLogin5(request):
    return render(request, 'login/restablecer_contrasena.html')

# ========== JUEGOS ==========
def mostrarVideogames(request):
    return render(request, 'html/juegos/trivia/index.html')

def mostrarVideogames11(request):
    return render(request, 'html/juegos/trivia/menu.html')

def mostrarVideogames12(request):
    return render(request, 'html/juegos/trivia/juego.html')

def mostrarVideogames13(request):
    return render(request, 'html/juegos/trivia/final.html')

# ========== REGISTRO DE USUARIO ==========
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForms(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']  # ← este es el bueno

                validate_password(password)

                user = UsuarioPersonalizado.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_active=False
                )

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                activation_link = f"http://localhost:8000/activar/{uid}/{token}/"

                message = render_to_string('html/correo_activacion.html', {
                    'user': user,
                    'activation_link': activation_link
                })

                email_message = EmailMessage(
                    subject='Activa tu cuenta en Walk App',
                    body=message,
                    to=[email]
                )
                email_message.content_subtype = "html"
                email_message.encoding = "utf-8"
                email_message.send()

                messages.success(request, 'Cuenta creada. Verifica tu correo electrónico para activarla.')
                return redirect('login')

            except Exception as e:
                messages.error(request, f'Error al crear usuario: {str(e)}')
        else:
            print(form.errors)  #depuración
            messages.error(request, 'Revisa los campos del formulario.')
    else:
        form = RegistroUsuarioForms()

    return render(request, 'mi_app_registro/registro.html', {'form': form})

# ========== ACTIVAR CUENTA ==========
def activar_cuenta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UsuarioPersonalizado.objects.get(pk=uid)
    except:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, '¡Cuenta activada! Ya puedes iniciar sesión.')
        return redirect('login')
    else:
        messages.error(request, 'El enlace de activación no es válido.')
        return redirect('mi_app_registro/registro')

# ========== LOGIN Y LOGOUT ==========
def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'mi_app_registro/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('mi_app_registro/login')

# ========== VISTAS DE ADMINISTRADOR ==========
@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

@staff_member_required
def admin_estadisticas(request):
    return render(request, 'admin/admin_estadisticas.html')

@staff_member_required
def admin_rutas(request):
    return render(request, 'admin/admin_rutas.html')

@staff_member_required
def admin_reportes(request):
    return render(request, 'admin/admin_reportes.html')

@user_passes_test(lambda u: u.is_superuser)
@login_required
def admin_usuarios(request):
    usuarios = UsuarioPersonalizado.objects.all().order_by('-date_joined') 
    return render(request, 'admin/admin_usuarios.html', {'usuarios': usuarios})

# ========== PERFIL USUARIO ==========
@login_required
def perfil_usuario(request):
    rutas_recorridas = RutaRecorrida.objects.filter(usuario=request.user)
    total_km = sum(r.ruta.longitud for r in rutas_recorridas)
    total_horas = len(rutas_recorridas) * 1  # Suponiendo 1h por ruta por ahora
    return render(request, 'html/perfil_usuario.html', {
        'usuario': request.user,
        'rutas_recorridas': rutas_recorridas,
        'total_km': total_km,
        'total_horas': total_horas,
    })

# ========== CRUD RUTAS ==========
def lista_rutas(request):
    rutas = Ruta.objects.all().order_by('nombre_ruta')
    return render(request, 'html/rutas.html', {'rutas': rutas})

def detalle_ruta(request, ruta_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    return render(request, 'html/rutas/detalle_ruta.html', {'ruta': ruta})

def crear_ruta(request):
    if request.method == 'POST':
        form = RutaForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_ruta = form.save()
            return redirect('rutas')
    else:
        form = RutaForm()
    return render(request, 'html/rutas/crear_ruta.html', {'form': form})

# ========== FAVORITOS ==========
def marcar_favorita(request, ruta_id, usuario_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    usuario = get_object_or_404(UsuarioPersonalizado, pk=usuario_id)
    if not UserRutaFavorita.objects.filter(usuario=usuario, ruta=ruta).exists():
        UserRutaFavorita.objects.create(usuario=usuario, ruta=ruta)
    return redirect('detalle_ruta', ruta_id=ruta.id)

def quitar_favorita(request, ruta_id, usuario_id):
    ruta = get_object_or_404(Ruta, pk=ruta_id)
    usuario = get_object_or_404(UsuarioPersonalizado, pk=usuario_id)
    UserRutaFavorita.objects.filter(usuario=usuario, ruta=ruta).delete()
    return redirect('detalle_ruta', ruta_id=ruta.id)

#==================
# COMUNIDAD
#==================

@login_required
def comunidad_view(request):
    publicaciones = Publicacion.objects.all().order_by('-fecha_publicacion')

    if request.method == 'POST':
        if 'comentario' in request.POST:
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.usuario = request.user
                comentario.publicacion_id = request.POST.get('publicacion_id')
                comentario.save()
                return redirect('comunidad')
        else:
            publicacion_form = PublicacionForm(request.POST, request.FILES)
            if publicacion_form.is_valid():
                publicacion = publicacion_form.save(commit=False)
                publicacion.usuario = request.user
                publicacion.save()
                return redirect('comunidad')
    else:
        publicacion_form = PublicacionForm()
        comentario_form = ComentarioForm()

    return render(request, 'html/comunidad.html', {
        'publicaciones': publicaciones,
        'publicacion_form': publicacion_form,
        'comentario_form': comentario_form,
    })