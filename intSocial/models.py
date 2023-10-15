from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    """
    Datos necesarios de un usuario
    """
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=255, unique=True)
    contasenia = models.CharField(max_length=60)
    esta_Activo = models.BooleanField(default=True)
    es_Admin = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Level(models.Model):
    """
    Nivel de privaciodad
    """
    name = models.CharField(max_length=50)  # 1 publico, 2 privado, 3 grupo


class Profile(models.Model):
    """
    Datos extras que tiene un usuario
    """
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10)
    imagen = models.CharField(max_length=255)
    imagen_header = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    info_contacto = models.TextField()
    email_publico = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username + ' ' + self.titulo


class Portafolio(models.Model):
    """
    También se les podrian considerar albums
    """
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username + ' ' + self.titulo


class Imagen(models.Model):
    """
    Datos para almacenar y hacer refencias a imagenes
    """
    src = models.ImageField(null=True, blank=True, upload_to="images/")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    portafolio = models.ForeignKey(Portafolio, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username + ' ' + self.titulo


class Post(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    receptor_type = models.IntegerField()
    post_type = models.IntegerField(default=1)

    def __str__(self):
        return self.autor.username + ' ' + self.titulo


class PostImagen(models.Model):
    """Muchos a muchos (Post-Imagen)"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)


class Likes(models.Model):
    """
    Likes y dislikes
    """
    valor = models.IntegerField()  # 1 like, 2 dislike
    ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.username + ' ' + self.creado_en


class Comentario(models.Model):
    """
    Para hacer comentarios
    """
    ref = models.ForeignKey(Post, on_delete=models.CASCADE)  # post en el que se encuentra
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    respuesta_a = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='respuestas')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' a ' + self.ref.autor.username


class Notificaciones(models.Model):
    not_type = models.IntegerField()  # 1 likes, 2 comentarios
    ref = models.ForeignKey(Post, on_delete=models.CASCADE)
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_recibe')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_envia')
    fue_leido = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)


class Grupos(models.Model):
    imagen = models.CharField(max_length=255)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField()  # 1 open, 2 closed
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
