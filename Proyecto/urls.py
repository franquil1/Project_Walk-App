"""
URL configuration for Proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Aplicacion import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # URL GENERALES

    
    path('', views.mostrarHome, name='home'),
    path('comunidad/', views.mostrarComunidad, name='comunidad'),
    path('rutas/', views.mostrarRutas, name='rutas'),
    path('juegos/', views.mostrarJuegos, name='juegos'),
    path('ranking/', views.mostrarRanking, name='ranking'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('', include(('Aplicacion.urls', 'Aplicacion'), namespace='Aplicacion')),




    # URL RUTAS

    path('morro/', views.mostrarMorro, name='morro'),
    path('cruces/', views.mostrarCruces, name='cruces'),
    path('torre24/', views.mostrarTorre24, name='torre24'),

    # ACCOUNT

    path('login/', views.mostrarLogin, name='login'),
    path('login2/', views.mostrarLogin2, name='login2'),
    path('login3/', views.mostrarLogin3, name='login3'),
    path('login5/', views.mostrarLogin5, name='login5'),

    # VIDEOGAMES

    # Trivia Home
    path('trivia/', views.mostrarVideogames, name='trivia_index'),
    # Trivia Menu
    path('trivia/menu/', views.mostrarVideogames11, name='trivia_menu'),
    # Trivia Juego
    path('trivia/juego/', views.mostrarVideogames12, name='trivia_juego'),
    # Trivia Final
    path('trivia/final/', views.mostrarVideogames13, name='trivia_final'),

]
