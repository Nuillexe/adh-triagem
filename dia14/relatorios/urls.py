from django.urls import path
from . import views

urlpatterns=[
    path('relatorios',views.painel_relatorio, name='relatorios'),
    path('relatorios/deletar/<int:paciente_id>/', views.deletar_participante,name='deletar_participante'),
    path('relatoris/pdf', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf')
]