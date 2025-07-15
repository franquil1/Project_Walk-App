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
