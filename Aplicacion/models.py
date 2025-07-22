from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, unique=True)
    correo_electronico = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)

    def __str__(self):
        return self.nombre_usuario

# modelo de rutas 


class Ruta(models.Model):
    nombre_ruta = models.CharField(max_length=255, verbose_name="Nombre de la Ruta")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    longitud = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Longitud (km)")
    dificultad_choices = [
        ('FACIL', 'Fácil'),
        ('MODERADO', 'Moderado'),
        ('DIFICIL', 'Difícil'),
        ('EXTREMO', 'Extremo'),
    ]
    dificultad = models.CharField(max_length=50, choices=dificultad_choices, default='MODERADO', verbose_name="Dificultad")
    duracion_estimada = models.CharField(max_length=100, blank=True, null=True, verbose_name="Duración Estimada")
    altitud_maxima = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Altitud Máxima (m)")
    ubicacion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ubicación")
    puntos_interes = models.TextField(blank=True, null=True, verbose_name="Puntos de Interés")
    coordenadas_inicio_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitud de Inicio")
    coordenadas_inicio_lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitud de Inicio")
    coordenadas_fin_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitud de Fin")
    coordenadas_fin_lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitud de Fin")
    
    # Relación Uno a Muchos: Una ruta es creada por un Usuario.
    # Si eliminas un Usuario, sus rutas creadas se establecerán a NULL en este campo.
    creada_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='rutas_creadas', verbose_name="Creada por")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    # Relación Muchos a Muchos: Usuarios pueden marcar rutas como favoritas.
    # Usamos un modelo 'through' explícito para poder añadir campos adicionales a la relación 
    # (como la fecha en que se añadió a favoritos).
    usuarios_favoritos = models.ManyToManyField(Usuario, through='UserRutaFavorita', related_name='rutas_favoritas', verbose_name="Marcada como Favorita por")

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"
        ordering = ['nombre_ruta'] # Ordena las rutas por nombre por defecto

    def __str__(self):
        return self.nombre_ruta

class UserRutaFavorita(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Asegura que un Usuario solo pueda marcar una Ruta como favorita una vez
        unique_together = ('usuario', 'ruta') 
        verbose_name = "Ruta Favorita de Usuario"
        verbose_name_plural = "Rutas Favoritas de Usuarios"

    def __str__(self):
        return f"{self.usuario.nombre_usuario} - {self.ruta.nombre_ruta}"