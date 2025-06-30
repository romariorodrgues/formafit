"""
URLs para sistema de notificações.
"""
from django.urls import path
from . import views

app_name = 'notificacoes'

urlpatterns = [
    # Dashboard de notificações
    path('', views.NotificacaoListView.as_view(), name='lista'),
    
    # Criar notificação manual
    path('nova/', views.NotificacaoCreateView.as_view(), name='criar'),
    path('<int:pk>/', views.NotificacaoDetailView.as_view(), name='detalhe'),
    path('<int:pk>/marcar-lida/', views.MarcarComoLidaView.as_view(), name='marcar_lida'),
    
    # Notificações automáticas
    path('automaticas/', views.NotificacaoAutomaticaListView.as_view(), name='automaticas'),
    path('automatica/<int:pk>/editar/', views.NotificacaoAutomaticaUpdateView.as_view(), name='automatica_editar'),
    
    # Tipos de notificação
    path('tipos/', views.TipoNotificacaoListView.as_view(), name='tipos'),
    path('tipo/novo/', views.TipoNotificacaoCreateView.as_view(), name='tipo_criar'),
    path('tipo/<int:pk>/editar/', views.TipoNotificacaoUpdateView.as_view(), name='tipo_editar'),
    
    # Configurações
    path('configuracoes/', views.ConfiguracoesNotificacaoView.as_view(), name='configuracoes'),
    path('aluno/<int:aluno_id>/configuracoes/', views.ConfiguracaoAlunoView.as_view(), name='configuracao_aluno'),
    
    # WhatsApp
    path('whatsapp/teste/', views.TesteWhatsAppView.as_view(), name='teste_whatsapp'),
    path('whatsapp/logs/', views.LogWhatsAppView.as_view(), name='logs_whatsapp'),
]
