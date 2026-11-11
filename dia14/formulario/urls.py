from django.urls import path
from . import views



urlpatterns=[
    path('formulario',views.cadastrar_participante, name='cadastrar_participante')
]

