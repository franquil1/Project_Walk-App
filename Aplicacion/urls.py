from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 

# ¡IMPORTANTE! app_name debe ser el nombre exacto de la carpeta de tu aplicación
app_name = 'mi_app_registro' # Si tu carpeta de app se llama 'Aplicacion'


urlpatterns = [
    path('home/', views.mostrarHome, name='home'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('registro/', views.registro_usuario, name='registro'),
    # urls de rutas
    path('rutas/', views.lista_rutas, name='rutas'),
    path('rutas/<int:ruta_id>/', views.detalle_ruta, name='detalle_ruta'),
    path('rutas/crear/', views.crear_ruta, name='crear_ruta'),
    path('rutas/<int:ruta_id>/favorito/<int:usuario_id>/', views.marcar_favorita, name='marcar_favorita'),
    path('rutas/<int:ruta_id>/quitar_favorito/<int:usuario_id>/', views.quitar_favorita, name='quitar_favorita'),
    #registro
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)