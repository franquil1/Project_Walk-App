from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views

#app_name = 'mi_app_registro'

# Nombre de tu app

urlpatterns = [ 
    path('home/', views.mostrarHome, name='home'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('registro/', views.registro_usuario, name='registro'),
    
    # URLs de rutas
    path('rutas/', views.lista_rutas, name='rutas'),
    path('rutas/<int:ruta_id>/', views.detalle_ruta, name='detalle_ruta'),
    path('rutas/crear/', views.crear_ruta, name='crear_ruta'),
    path('rutas/<int:ruta_id>/favorito/<int:usuario_id>/', views.marcar_favorita, name='marcar_favorita'),
    path('rutas/<int:ruta_id>/quitar_favorito/<int:usuario_id>/', views.quitar_favorita, name='quitar_favorita'),

    # Activación de cuenta por correo
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),

    # Perfil de usuario
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),

    # ===============================
    # 📬 RECUPERAR CONTRASEÑA
    # ===============================

    # 1. Formulario para ingresar correo
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='login2/password_reset.html'), name='password_reset'),

    # 2. Mensaje de que se envió el correo
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='login2/password_reset_done.html'), name='password_reset_done'),

    # 3. Formulario para ingresar nueva contraseña desde el correo
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='login2/password_reset_confirm.html'), name='password_reset_confirm'),

    # 4. Confirmación de que la contraseña fue cambiada
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='login2/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
