# Register your models here.
from django.contrib import admin
from .models import Usuario, Ruta, UserRutaFavorita 

admin.site.register(Usuario)
admin.site.register(Ruta)
admin.site.register(UserRutaFavorita)