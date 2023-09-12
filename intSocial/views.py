from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Usuario
from .forms import CrearNuevoUsuario
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
        