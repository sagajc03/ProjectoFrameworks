from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name="index"),
    path('login/', views.signin, name="login"),
    path('signup/', views.signup, name="signup"),
    path('timeline/', views.timeline, name="timeline"),
    path('post/<int:id_post>', views.post, name="post_details"),
    path('newpost/', views.new_post, name="new_post"),
    path('usuario/', views.usuario, name="usuario"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.signout, name='logout'),
    path('profile/settings/', views.profile_settings, name="profile_settings")
]
