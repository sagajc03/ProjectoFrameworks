from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>index</h1>")

def login(request):
    return HttpResponse("<h1>login</h1>")

def signup(request):
    return HttpResponse("<h1>Sign up</h1>")

def time_line(request):
    return HttpResponse("<h1>Time Line</h1>")

def post(request):
    return HttpResponse("<h1>post</h1>")

def new_post(request):
    return HttpResponse("<h1>New post</h1>")

def profile(request):
    return HttpResponse("<h1>Perfil</h1>")