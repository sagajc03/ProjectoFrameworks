from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('usuario/', views.usuario),
    path('crear_usuario/', views.crear_usuario),
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('timeline/', views.timeline, name="timeline"),
    path('post/<int:id_post>', views.post, name="post_details"),
    path('newpost/', views.new_post, name="new_post"),
    path('profile/<int:id_profile>', views.profile, name="profile_details")
]
