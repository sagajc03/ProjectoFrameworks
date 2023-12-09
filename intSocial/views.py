from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from .models import Usuario, Post, Comentario, Imagen, PostImagen, Profile, Likes, Notificaciones
from .forms import CreateNewPost, CrearNuevoUsuario, CreateNewComment, UpdateUserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count, Case, When, IntegerField
from django.views.decorators.http import require_POST

# Create your views here.

def index(request):
    """
    Inicio que tiene un poco de informacion
    """
    title = 'Soy el inicio awebito'
    return render(request, "index.html", {
        'title': title
    })


def usuario(request):
    return render(request, "usuario.html", {

    })


def signup(request):
    """
    Pagina que te permite crear un nuevo usuario
    Despues de crear usuario inicia sesion haciendo
    uso de los metodos de django
    """
    if request.method == 'GET':
        return render(request, 'crear_usuario.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(request, 'crear_usuario.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exist'
                })
        return render(request, 'crear_usuario.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })


def signin(request):
    """
    Iniciar sesion en la pagina usando los metodos
    de django
    """
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('timeline')

def signout(request):
    """
    Sale de la sesion usando metodo de django
    """
    logout(request)
    return redirect('index')


@login_required
def timeline(request):
    """
    Crea un paginator para mostrar 10 publicaciones a la vez,
    se debe de estar logeado para ver
    """
    non_read_notis= Notificaciones.objects.filter(receptor=request.user, fue_leido=False).count()
    all_images = Imagen.objects.all()
    relaciones = PostImagen.objects.all()
    all_posts = Post.objects.annotate(
    cantidad_likes=Count(Case(When(likes__valor=1, then=1))),
    cantidad_dislikes=Count(Case(When(likes__valor=2, then=1)))
    ).order_by('-creado_en')
    

    for imagen in all_images:
        imagen.src = imagen.src.url

        # Crea una instancia de Paginator para paginar los objetos
    paginator = Paginator(all_posts, 10)  # Muestra 10 publicaciones por página

    page = request.GET.get('page')
    try:
        posts_pagina = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        posts_pagina = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, muestra la última página
        posts_pagina = paginator.page(paginator.num_pages)

    context = {
        'posts': posts_pagina,
        'imagenes': all_images,
        'relaciones': relaciones,
        'non_read_notis':non_read_notis,
    }
    return render(request, 'timeline.html', context)


@login_required
def post(request, id_post):
    """
    Permite entrar a los detallaes de una publicacion y
    permite tambien poner un comentario en dicha publicacion
    """
    non_read_notis= Notificaciones.objects.filter(receptor=request.user, fue_leido=False).count()
    post = get_object_or_404(Post, id=id_post)

    cantidad_likes = Likes.objects.filter(valor=1, ref=post).count()
    cantidad_dislikes = Likes.objects.filter(valor=2, ref=post).count()

    all_images = Imagen.objects.all()
    relaciones = PostImagen.objects.all()
    comentarios = Comentario.objects.filter(ref_id=id_post).order_by('creado_en')

    for imagen in all_images:
        imagen.src = imagen.src.url

    if request.method == 'GET':

        return render(request, 'detalles_post.html', {
            'post': post,
            'comentarios': comentarios,
            'form': CreateNewComment,
            'imagenes': all_images,
            'relaciones': relaciones,
            'cantidad_likes':cantidad_likes,
            'cantidad_dislikes':cantidad_dislikes,
            'non_read_notis':non_read_notis,
        })
    else:
        Comentario.objects.create(ref=post, user=request.user, contenido=request.POST['contenido'])
        Notificaciones.objects.create(not_type=2, ref=post, receptor=post.autor, sender=request.user)
        comentarios = Comentario.objects.filter(ref_id=id_post).order_by('-creado_en')

        return render(request, 'detalles_post.html', {
            'post': post,
            'comentarios': comentarios,
            'form': CreateNewComment,
            'imagenes': all_images,
            'relaciones': relaciones,
            'cantidad_likes':cantidad_likes,
            'cantidad_dislikes':cantidad_dislikes,
            'non_read_notis':non_read_notis,
        })


@login_required
def new_post(request):
    """
    Permite crear una publicacion, se pueden añadir una imagen
    """
    non_read_notis= Notificaciones.objects.filter(receptor=request.user, fue_leido=False).count()
    if request.method == 'GET':
        return render(request, 'new_post.html', {
            'non_read_notis':non_read_notis,
            'form': CreateNewPost()
        })
    else:
        if not request.FILES:
            Post.objects.create(titulo=request.POST['titulo'], contenido=request.POST['contenido'],
                                autor=request.user, level_id=1, receptor_type=1,categoria=request.POST['categoria'])
            return redirect('timeline')
        else:
            post = Post.objects.create(titulo=request.POST['titulo'], contenido=request.POST['contenido'],
                                       autor=request.user, level_id=1, receptor_type=1, categoria=request.POST['categoria'])
            imagen = Imagen.objects.create(src=request.FILES['imagen'],
                                           titulo=request.POST['titulo'], descripcion=request.POST['contenido'],
                                           usuario=request.user, level_id=1)
            postimg = PostImagen.objects.create(post=post, imagen=imagen)
            return redirect('timeline')

@login_required
def profile(request, username=None):
    """
    Permite ver las publicaciones del usuario
    y la informacion personal que este haya compartido
    """
    non_read_notis= Notificaciones.objects.filter(receptor=request.user, fue_leido=False).count()
    user = get_object_or_404(User, username=username)
    try:
        perfil = Profile.objects.get(usuario=user)
    except Profile.DoesNotExist:
        perfil = Profile.objects.create(usuario=user)

    posts = Post.objects.annotate(
    cantidad_likes=Count(Case(When(likes__valor=1, then=1), output_field=IntegerField())),
    cantidad_dislikes=Count(Case(When(likes__valor=2, then=1), output_field=IntegerField()))
    ).filter(autor=user).order_by('-creado_en')
    all_images = Imagen.objects.all()
    relaciones = PostImagen.objects.all()

    for imagen in all_images:
        imagen.src = imagen.src.url

    return render(request, 'profile.html', {
        'profile': perfil,
        'user': user,
        'posts': posts,
        'imagenes': all_images,
        'relaciones': relaciones,
        'non_read_notis':non_read_notis,
    })

def test(request):
    """
    Pagina de test, no hay nada mas que el menu
    """
    return render(request, 'layouts/base.html',{
        'request':request
    })

@login_required
def profile_settings(request):
    """
    Permite modificar opciones del perfil (profile) y acceso a 
    modificar cosas del usuario (django User)
    """
    non_read_notis= Notificaciones.objects.filter(receptor=request.user, fue_leido=False).count()
    if request.method == 'GET':
        try:
            perfil = Profile.objects.get(usuario=request.user)
        except Profile.DoesNotExist:
            perfil = Profile.objects.create(usuario=request.user)
        return render(request, 'profiles_settings.html', {
            'perfil': perfil,
            'non_read_notis':non_read_notis,
        })
    else:
        #Codigo para guardar los datos del perfil
        perfil = Profile.objects.get(usuario=request.user)

        perfil.titulo = request.POST['titulo']
        perfil.bio = request.POST['bio']

        fecha_nacimiento_str = request.POST.get('fecha_nacimiento', '')
        try:
            perfil.fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%m/%d/%Y').date()
        except ValueError:
            perfil.fecha_nacimiento = None

        perfil.info_contacto = request.POST['info_contacto']
        perfil.email_publico = request.POST['email_publico']

        if 'imagen' in request.FILES:
            perfil.imagen = request.FILES['imagen']
        if 'imagen_header' in request.FILES:
            perfil.imagen_header = request.FILES['imagen_header']

        try:
            perfil.save()
            messages.success(request, 'Profile succesfuly updated.')
        except Exception as e:
            messages.error(request, f'An error happened')

        return redirect('profile', username=request.user.username)

@login_required
def user_settings(request):
    """
    Configurar cosas del usuario haciendo uso 
    de metodos de django
    """
    non_read_notis= Notificaciones.objects.filter(receptor=request.user, fue_leido=False).count()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            return redirect('profile', username=request.user.username)
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'user_settings.html', {'user_form': user_form,
                                                  'non_read_notis':non_read_notis,})

@login_required
def search(request, categoria='Off-topic'):
    """
    Buscar post en base a las categorias preestablecidas
    """
    non_read_notis= Notificaciones.objects.filter(receptor=request.user, fue_leido=False).count()
    posts = Post.objects.annotate(
    cantidad_likes=Count(Case(When(likes__valor=1, then=1), output_field=IntegerField())),
    cantidad_dislikes=Count(Case(When(likes__valor=2, then=1), output_field=IntegerField()))
    ).filter(categoria=categoria).order_by('-creado_en')
    all_images = Imagen.objects.all()
    relaciones = PostImagen.objects.all()

    for imagen in all_images:
        imagen.src = imagen.src.url

    return render(request, 'search.html', {
        'posts': posts,
        'imagenes': all_images,
        'relaciones': relaciones,
        'non_read_notis':non_read_notis,
    })

@login_required
def notificaciones(request):
    """
    Permite leer las notificaciones recibidas (por como estan configuradas,
    solo son los comentarios que reciben tus post)
    """
    non_read_notis= Notificaciones.objects.filter(receptor=request.user, fue_leido=False).count()
    notis = Notificaciones.objects.filter(receptor=request.user).order_by('-creado_en')
    notis.update(fue_leido=True)
    return render(request, 'notificaciones.html',{
        'notis':notis,
        'non_read_notis':non_read_notis,
    })


@require_POST
def incrementar_like(request, post_id):
    """
    Paso intermedio, crea un like sobre una publicacion, quita el dislike en caso de haberlo
    """
    publicacion = get_object_or_404(Post, pk=post_id)
    if Likes.objects.filter(usuario=request.user, ref=publicacion, valor=2).exists():
        quitar_like_dislike(request, post_id, 2)
    Likes.objects.get_or_create(usuario=request.user, ref=publicacion, valor=1)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def incrementar_dislike(request, post_id):
    """
    Paso intermedio, crea un dislike sobre una publicacion, quita el like en caso de haberlo
    """
    publicacion = get_object_or_404(Post, pk=post_id)
    if Likes.objects.filter(usuario=request.user, ref=publicacion, valor=1).exists():
        quitar_like_dislike(request, post_id, 1)
    Likes.objects.get_or_create(usuario=request.user, ref=publicacion, valor=2)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def quitar_like(request, post_id):
    """
    quita un like
    """
    quitar_like_dislike(request, post_id, 1)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def quitar_dislike(request, post_id):
    """
    quita un dislike
    """
    quitar_like_dislike(request, post_id, 2)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def quitar_like_dislike(request, post_id, tipo):
    """
    borra sobre la base de datos el like o dislike
    """
    publicacion = get_object_or_404(Post, pk=post_id)
    Likes.objects.filter(usuario=request.user, ref=publicacion, valor=tipo).delete()