from django.urls import path
from . import views

# ¡IMPORTANTE! app_name debe ser el nombre exacto de la carpeta de tu aplicación
app_name = 'mi_app_registro' # Si tu carpeta de app se llama 'Aplicacion'

urlpatterns = [
    path('home/', views.mostrarHome, name='home'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('registro/', views.registro_usuario, name='registro'),
]
