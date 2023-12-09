from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name="index"), #index, mas informacion que otra cosa
    path('login/', views.signin, name="login"), #login, sirve para logearse
    path('signup/', views.signup, name="signup"), #sirve para crear una cuenta
    path('timeline/', views.timeline, name="timeline"), #permite ver las publicaciones recientes
    path('post/<int:id_post>/', views.post, name="post_details"), #permite ver un post individual y comentarlo
    path('newpost/', views.new_post, name="new_post"), #permite crear un post nuevo
    path('usuario/', views.usuario, name="usuario"), #no hace nada 
    path('profile/<str:username>/', views.profile, name="profile"), #permite ver el perfil de un usuario
    path('logout/', views.signout, name='logout'), #te deslogea
    path('profile_settings/', views.profile_settings, name="profile_settings"), #permite modificar cosas del perfil
    path('user_settings', views.user_settings, name='user_settings'), #cambias cosas del perfil como nombre de usuario
    path('test/', views.test), #test
    path('search/<str:categoria>',views.search, name="search"), #permite buscar en base a palabras clave
    path('notifications/', views.notificaciones, name='notifications'), #permite ver las notificaciones recibidas
    path('incrementar_like/<int:post_id>/', views.incrementar_like, name='incrementar_like'), #incrementa el like de un post
    path('quitar_like/<int:post_id>/', views.quitar_like, name='quitar_like'), #quita el like a un post
    path('incrementar_dislike/<int:post_id>/', views.incrementar_dislike, name='incrementar_dislike'), #da dislike a un post
    path('quitar_dislike/<int:post_id>/', views.quitar_dislike, name='quitar_dislike'), #quita el dislike a post
]
