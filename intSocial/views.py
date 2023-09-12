from django.shortcuts import render, redirect,redirect
from django.http import HttpResponse
from .models import Usuario, Post
from .forms import CrearNuevoUsuario, CreateNewPost


# Create your views here.

def index(request):
    title= 'Soy el inicio awebito'
    return render(request, "index.html",{
        'title': title
    })


def usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuario.html",{
        'usuarios': usuarios
    })
    

def crear_usuario(request):
    if request.method == 'GET':
        return render(request, 'crear_usuario.html', {
            'form': CrearNuevoUsuario
        })
    else:
        Usuario.objects.create(
            nombre=request.POST['nombre'],
            apellidos=request.POST['apellidos'],
            username=request.POST['username'],
            email=request.POST['email'],
            contasenia=request.POST['contasenia'])
        return render(request, 'crear_usuario.html',{
            'form': CrearNuevoUsuario
        })
        
    return HttpResponse("<h1>index</h1>")


def login(request):
    return HttpResponse("<h1>login</h1>")


def signup(request):
    return HttpResponse("<h1>Sign up</h1>")


def timeline(request):
    posts = Post.objects.all()
    return render(request, 'timeline.html', {
        'posts':posts
    })


def post(request, id_post):
    return HttpResponse("<h1>post %i</h1>" % id_post)


def new_post(request):
    if request.method == 'GET':
        return render(request, 'new_post.html', {
            'form': CreateNewPost()
        })
    else:
        Post.objects.create(titulo=request.POST['titulo'], contenido=request.POST['contenido'], autor_id = 1, level_id = 1, receptor_type = 1)
        return redirect('timeline')


def profile(request, id_profile):
    return HttpResponse("<h1>Perfil %i</h1>" %id_profile)
