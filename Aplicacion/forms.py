from django import forms
from .models import Usuario
from .models import Ruta


class RegistroUsuarioForms(forms.ModelForm):
    contraseña2 = forms.CharField(label = 'Confirmar contraseña', widget= forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'correo_electronico', 'contraseña']
        widgets = {
            'constraseña': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get('contraseña')
        contraseña2 = cleaned_data.get('contraseña2')

        if contraseña and contraseña2 and contraseña != contraseña2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    

# Nuevo formulario para el login
class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

# creacion de la ruta 

class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ['nombre_ruta', 'descripcion', 'longitud', 'dificultad', 
                  'duracion_estimada', 'altitud_maxima', 'ubicacion', 
                  'puntos_interes', 'coordenadas_inicio_lat', 'coordenadas_inicio_lon',
                  'coordenadas_fin_lat', 'coordenadas_fin_lon']
        # No incluyas 'creada_por', 'fecha_creacion' ni 'usuarios_favoritos' aquí,
        # ya que se gestionan automáticamente o en la vista.