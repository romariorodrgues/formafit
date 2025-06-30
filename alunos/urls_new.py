"""
URLs para gerenciamento de alunos.
"""
from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    # Lista e cadastro
    path('', views.AlunosListView.as_view(), name='lista'),
    path('cadastrar/', views.AlunoCreateView.as_view(), name='cadastrar'),
    
    # Detalhes e edição
    path('<int:pk>/', views.AlunoDetailView.as_view(), name='detalhes'),
    path('<int:pk>/editar/', views.AlunoUpdateView.as_view(), name='editar'),
    path('<int:pk>/toggle-status/', views.toggle_status, name='toggle_status'),
    
    # Medidas corporais
    path('<int:pk>/medidas/', views.historico_medidas, name='historico_medidas'),
    path('<int:pk>/medidas/adicionar/', views.adicionar_medidas, name='adicionar_medidas'),
    
    # Fotos de progresso
    path('<int:pk>/fotos/', views.galeria_fotos, name='galeria_fotos'),
    path('<int:pk>/fotos/adicionar/', views.adicionar_foto, name='adicionar_foto'),
    
    # Estatísticas
    path('<int:pk>/estatisticas/', views.estatisticas_aluno, name='estatisticas'),
]
