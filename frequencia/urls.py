"""
URLs para controle de frequência.
"""
from django.urls import path
from . import views

app_name = 'frequencia'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_frequencia, name='dashboard'),
    
    # Registros de Presença
    path('registros/', views.FrequenciaListView.as_view(), name='lista'),
    path('registros/novo/', views.RegistroPresencaCreateView.as_view(), name='registrar_presenca'),
    
    # Agendamentos
    path('agenda/', views.AgendaListView.as_view(), name='agenda'),
    path('agenda/nova/', views.AgendaCreateView.as_view(), name='agendar_aula'),
    path('agenda/<int:agenda_id>/status/', views.alterar_status_agenda, name='alterar_status'),
    
    # Calendário
    path('calendario/', views.calendario_mensal, name='calendario'),
    
    # Relatórios
    path('relatorio/<int:aluno_id>/', views.relatorio_frequencia_aluno, name='relatorio_aluno'),
]
