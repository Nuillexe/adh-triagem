from django.urls import path
from . import views

urlpatterns = [
    path('', views.logar_usuario, name='login'),
    path('logout/', views.deslogar_usuario, name='logout'),
]