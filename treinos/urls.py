"""
URLs para gerenciamento de treinos e exercícios.
"""
from django.urls import path
from . import views

app_name = 'treinos'

urlpatterns = [
    # Exercícios
    path('exercicios/', views.ExercicioListView.as_view(), name='exercicios'),
    path('exercicios/criar/', views.ExercicioCreateView.as_view(), name='criar_exercicio'),
    
    # Planos de Treino
    path('', views.PlanoTreinoListView.as_view(), name='planos'),
    path('criar/', views.PlanoTreinoCreateView.as_view(), name='criar'),
    path('<int:pk>/', views.PlanoTreinoDetailView.as_view(), name='detalhes_plano'),
    path('<int:plano_id>/copiar/', views.copiar_plano_treino, name='copiar_plano'),
    path('<int:plano_id>/ativar/', views.ativar_plano_treino, name='ativar_plano'),
    
    # Dias de Treino
    path('<int:plano_id>/dia/', views.criar_treino_diario, name='criar_treino_diario'),
    path('dia/<int:treino_id>/exercicio/', views.adicionar_exercicio_treino, name='adicionar_exercicio'),
]
