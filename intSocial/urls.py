from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name="index"),
    path('login/', views.signin, name="login"),
    path('signup/', views.signup, name="signup"),
    path('timeline/', views.timeline, name="timeline"),
    path('post/<int:id_post>/', views.post, name="post_details"),
    path('newpost/', views.new_post, name="new_post"),
    path('usuario/', views.usuario, name="usuario"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('logout/', views.signout, name='logout'),
    path('profile_settings/', views.profile_settings, name="profile_settings"),
    path('user_settings', views.user_settings, name='user_settings'),
    path('test/', views.test),
    path('search/<str:categoria>',views.search, name="search"),
    path('notifications/', views.notificaciones, name='notifications'),
    path('incrementar_like/<int:post_id>/', views.incrementar_like, name='incrementar_like'),
    path('quitar_like/<int:post_id>/', views.quitar_like, name='quitar_like'),
    path('incrementar_dislike/<int:post_id>/', views.incrementar_dislike, name='incrementar_dislike'),
    path('quitar_dislike/<int:post_id>/', views.quitar_dislike, name='quitar_dislike'),
]
