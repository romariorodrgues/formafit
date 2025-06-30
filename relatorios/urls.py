"""
URLs para geração de relatórios.
"""
from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    # Lista de relatórios
    path('', views.RelatorioListView.as_view(), name='lista'),
    
    # Gerar relatórios
    path('gerar/<int:aluno_id>/', views.GerarRelatorioView.as_view(), name='gerar'),
    path('gerar-multiplos/', views.GerarRelatoriosMultiplosView.as_view(), name='gerar_multiplos'),
    
    # Visualizar e download
    path('<uuid:pk>/', views.RelatorioDetailView.as_view(), name='detalhe'),
    path('<uuid:pk>/download/', views.DownloadRelatorioView.as_view(), name='download'),
    path('<uuid:pk>/enviar-email/', views.EnviarRelatorioEmailView.as_view(), name='enviar_email'),
]
