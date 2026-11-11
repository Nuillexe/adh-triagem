from django.urls import path
from . import views

urlpatterns=[
    path('relatorios',views.painel_relatorio, name='relatorios'),
    path('deletar/<int:participante_id>/', views.deletar_participante, name='deletar_participante')
]