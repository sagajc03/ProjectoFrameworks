from django import forms

class CrearNuevoUsuario(forms.Form):
    nombre=forms.CharField(label='Nombre', max_length=50)
    apellidos=forms.CharField(label='Apellidos', max_length=50)
    username=forms.CharField(label='Nombre de Usuario', max_length=50)
    email=forms.CharField(label='Correo Elctronico', max_length=255)
    contasenia=forms.CharField(label='Contraseña', max_length=60)

class CreateNewPost(forms.Form):
    titulo = forms.CharField(label="Titulo",  max_length=50, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    contenido = forms.CharField(label="Detalles", widget=forms.TextInput(attrs={
        'class': 'input'
    }))


class CreateNewComment(forms.Form):
    contenido = forms.CharField(label="Escribe tu comentario", widget=forms.TextInput(attrs={
        'class': 'input'
    }))