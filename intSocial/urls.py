from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/login', views.login),
    path('/signup', views.signup),
    path('/TimeLine', views.time_line),
    path('/post', views.post),
    path('/newpost', views.new_post),
    path('/profile', views.profile)
]
