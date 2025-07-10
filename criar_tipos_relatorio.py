#!/usr/bin/env python
"""
Script para criar tipos de relatório padrão no sistema.
"""
import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from relatorios.models import TipoRelatorio

def criar_tipos_relatorio():
    """Cria tipos de relatório padrão no sistema."""
    
    tipos_padrao = [
        {
            'nome': 'Relatório Completo de Progresso',
            'descricao': 'Relatório completo com medidas corporais, frequência, gráficos e fotos de evolução.',
            'template_filename': 'relatorio_completo.html',
            'ativo': True,
            'incluir_graficos': True,
            'incluir_fotos': True,
            'incluir_medidas': True,
            'incluir_frequencia': True,
        },
        {
            'nome': 'Relatório de Medidas Corporais',
            'descricao': 'Foco nas medidas corporais e evolução do peso, IMC e circunferências.',
            'template_filename': 'relatorio_medidas.html',
            'ativo': True,
            'incluir_graficos': True,
            'incluir_fotos': False,
            'incluir_medidas': True,
            'incluir_frequencia': False,
        },
        {
            'nome': 'Relatório de Frequência',
            'descricao': 'Análise da frequência de treinos e assiduidade do aluno.',
            'template_filename': 'relatorio_frequencia.html',
            'ativo': True,
            'incluir_graficos': True,
            'incluir_fotos': False,
            'incluir_medidas': False,
            'incluir_frequencia': True,
        },
        {
            'nome': 'Relatório Visual com Fotos',
            'descricao': 'Relatório visual com fotos de evolução e gráficos comparativos.',
            'template_filename': 'relatorio_visual.html',
            'ativo': True,
            'incluir_graficos': True,
            'incluir_fotos': True,
            'incluir_medidas': True,
            'incluir_frequencia': False,
        },
        {
            'nome': 'Relatório Simples',
            'descricao': 'Relatório básico com informações essenciais de progresso.',
            'template_filename': 'relatorio_simples.html',
            'ativo': True,
            'incluir_graficos': False,
            'incluir_fotos': False,
            'incluir_medidas': True,
            'incluir_frequencia': True,
        }
    ]
    
    print("=== CRIANDO TIPOS DE RELATÓRIO ===")
    
    for tipo_data in tipos_padrao:
        tipo, created = TipoRelatorio.objects.get_or_create(
            nome=tipo_data['nome'],
            defaults=tipo_data
        )
        
        if created:
            print(f"✓ Criado: {tipo.nome}")
        else:
            print(f"• Já existe: {tipo.nome}")
    
    print(f"\n=== RESUMO ===")
    total_tipos = TipoRelatorio.objects.count()
    tipos_ativos = TipoRelatorio.objects.filter(ativo=True).count()
    print(f"Total de tipos cadastrados: {total_tipos}")
    print(f"Tipos ativos: {tipos_ativos}")
    
    print("\n=== TIPOS DISPONÍVEIS ===")
    for tipo in TipoRelatorio.objects.filter(ativo=True):
        print(f"- {tipo.nome}")
        print(f"  Descrição: {tipo.descricao}")
        caracteristicas = []
        if tipo.incluir_graficos:
            caracteristicas.append("Gráficos")
        if tipo.incluir_fotos:
            caracteristicas.append("Fotos")
        if tipo.incluir_medidas:
            caracteristicas.append("Medidas")
        if tipo.incluir_frequencia:
            caracteristicas.append("Frequência")
        print(f"  Inclui: {', '.join(caracteristicas)}")
        print()

if __name__ == '__main__':
    criar_tipos_relatorio()
