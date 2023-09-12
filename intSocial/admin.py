from django.contrib import admin
from .models import Usuario, Grupos, Imagen, Portafolio, Post, PostImagen, Profile, Level, Likes, Comentario, Notificaciones

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Grupos)
admin.site.register(Imagen)
admin.site.register(Portafolio)
admin.site.register(Post)
admin.site.register(PostImagen)
admin.site.register(Profile)
admin.site.register(Level)
admin.site.register(Likes)
admin.site.register(Comentario)
admin.site.register(Notificaciones)
