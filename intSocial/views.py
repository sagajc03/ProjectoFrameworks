from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("<h1>index</h1>")


def login(request):
    return HttpResponse("<h1>login</h1>")


def signup(request):
    return HttpResponse("<h1>Sign up</h1>")


def timeline(request):
    return render(request, 'timeline.html')


def post(request, id_post):
    return HttpResponse("<h1>post %i</h1>" % id_post)


def new_post(request):
    return HttpResponse("<h1>New post</h1>")


def profile(request, id_profile):
    return HttpResponse("<h1>Perfil %i</h1>" %id_profile)
