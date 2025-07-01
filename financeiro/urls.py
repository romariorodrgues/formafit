"""
URLs para gestão financeira.
"""
from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_financeiro, name='dashboard'),
    
    # Faturas
    path('faturas/', views.lista_faturas, name='lista_faturas'),
    path('faturas/<int:pk>/', views.fatura_detail, name='fatura_detail'),
    path('faturas/criar/', views.criar_fatura, name='criar_fatura'),
    path('faturas/gerar-automaticas/', views.gerar_faturas_automaticas, name='gerar_faturas_automaticas'),
    
    # Pagamentos
    path('faturas/<int:fatura_id>/pagar/', views.registrar_pagamento, name='registrar_pagamento'),
    
    # Contratos
    path('contratos/', views.lista_contratos, name='lista_contratos'),
    path('contratos/criar/', views.criar_contrato, name='criar_contrato'),
    path('contratos/<int:pk>/', views.contrato_detail, name='contrato_detail'),
    
    # Planos
    path('planos/', views.lista_planos, name='lista_planos'),
    path('planos/criar/', views.criar_plano, name='criar_plano'),
    path('planos/<int:pk>/editar/', views.editar_plano, name='editar_plano'),
    path('planos/<int:pk>/deletar/', views.deletar_plano, name='deletar_plano'),
    
    # Relatórios
    path('relatorio/', views.relatorio_financeiro, name='relatorio_financeiro'),
    path('inadimplencia/', views.inadimplencia_view, name='inadimplencia'),
    
    # AJAX
    path('ajax/estatisticas/<int:mes>/<int:ano>/', views.ajax_estatisticas_mes, name='ajax_estatisticas_mes'),
    path('ajax/grafico-receita/', views.ajax_dados_grafico_receita, name='ajax_grafico_receita'),
    path('ajax/contrato/<int:pk>/update/', views.ajax_update_contrato, name='ajax_update_contrato'),
    path('ajax/plano/<int:pk>/details/', views.ajax_plano_details, name='ajax_plano_details'),
    path('ajax/plano/<int:pk>/delete/', views.ajax_delete_plano, name='ajax_delete_plano'),
]
