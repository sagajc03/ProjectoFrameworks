from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from .models import Usuario, Post, Comentario, Imagen, PostImagen, Profile
from .forms import CreateNewPost, CrearNuevoUsuario, CreateNewComment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages



# Create your views here.

def index(request):
    title = 'Soy el inicio awebito'
    return render(request, "index.html", {
        'title': title
    })


def usuario(request):

    return render(request, "usuario.html", {

    })


def signup(request):
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
    logout(request)
    return redirect('index')


@login_required
def timeline(request):
    all_posts = Post.objects.all().order_by('-creado_en')
    all_images = Imagen.objects.all()
    relaciones = PostImagen.objects.all()

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
    }
    return render(request, 'timeline.html', context)


@login_required
def post(request, id_post):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=id_post)
        imagenes_relacionadas = PostImagen.objects.filter(post=post)
        comentarios = Comentario.objects.filter(ref_id=id_post).order_by('creado_en')
        return render(request, 'detalles_post.html', {
            'post': post,
            'comentarios': comentarios,
            'form': CreateNewComment,
            'imagenes_relacionadas': imagenes_relacionadas
        })
    else:
        post = get_object_or_404(Post, id=id_post)
        imagenes_relacionadas = PostImagen.objects.filter(post=post)
        Comentario.objects.create(ref=post, user=request.user, contenido=request.POST['contenido'])
        comentarios = Comentario.objects.filter(ref_id=id_post).order_by('-creado_en')
        return render(request, 'detalles_post.html', {
            'post': post,
            'comentarios': comentarios,
            'form': CreateNewComment,
            'imagenes_relacionadas': imagenes_relacionadas
        })


@login_required
def new_post(request):
    if request.method == 'GET':
        return render(request, 'new_post.html', {
            'form': CreateNewPost()
        })
    else:
        if not request.FILES:
            Post.objects.create(titulo=request.POST['titulo'], contenido=request.POST['contenido'],
                                autor=request.user, level_id=1, receptor_type=1)
            return redirect('timeline')
        else:
            post = Post.objects.create(titulo=request.POST['titulo'], contenido=request.POST['contenido'],
                                       autor=request.user, level_id=1, receptor_type=1)
            imagen = Imagen.objects.create(src=request.FILES['imagen'],
                                           titulo=request.POST['titulo'], descripcion=request.POST['contenido'],
                                           usuario=request.user, level_id=1)
            postimg = PostImagen.objects.create(post=post, imagen=imagen)
            return redirect('timeline')


@login_required
def profile(request):
    user = request.user
    try:
        perfil = Profile.objects.get(usuario=request.user)
    except Profile.DoesNotExist:
        perfil = Profile.objects.create(usuario=request.user)

    return render(request, 'profile.html', {
        'profile': perfil,
        'user':user
    })


@login_required
def profile_settings(request):
    if request.method == 'GET':
        try:
            perfil = Profile.objects.get(usuario=request.user)
        except Profile.DoesNotExist:
            perfil = Profile.objects.create(usuario=request.user)
        return render(request, 'profiles_settings.html', {
            'perfil': perfil
        })
    else:
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

        return redirect('profile')