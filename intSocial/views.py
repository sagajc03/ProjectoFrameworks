from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Usuario, Post
from .forms import CreateNewPost, CrearNuevoUsuario

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
    

def signup(request):
    if request.method == 'GET':
        return render(request, 'crear_usuario.html', {
            'form': CrearNuevoUsuario
        })
    else:
        Usuario.objects.create_user(
            nombre=request.POST['nombre'],
            apellidos=request.POST['apellidos'],
            username=request.POST['username'],
            email=request.POST['email'],
            contasenia=request.POST['contasenia'])
        return redirect('/')
    


def login(request):
    if request.method == "GET":
        if 'logged_in' in request.COOKIES and 'username' in request.COOKIES:
            context = {
                'username':request.COOKIES['username'],
                'login_status':request.COOKIES.get('logged_in'),
            }
            return render(request, 'profile.html', context)
        else:
            return render(request, 'login.html')

    if request.method == "POST":
        username=request.POST.get('email')
        context = {
                'username':username,
                'login_status':'TRUE',
            }
        response = render(request, 'profile.html', context)

        # setting cookies
        response.set_cookie('username', username)
        response.set_cookie('logged_in', True)
        return response

def logout(request):
    response = HttpResponseRedirect(reverse('login'))

    response.delete_cookie('username')
    response.delete_cookie('logged_in')

    return response


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


def profile(request):
    if 'logged_in' in request.COOKIES and 'username' in request.COOKIES:
            context = {
                'username':request.COOKIES['username'],
                'login_status':request.COOKIES.get('logged_in'),
            }
            return render(request, 'profile.html', context)
    else:
        return render(request, 'profile.html')
