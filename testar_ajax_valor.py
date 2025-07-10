#!/usr/bin/env python
"""
Script para testar a funcionalidade AJAX de obter valor do contrato.
"""
import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from django.contrib.auth import get_user_model
from alunos.models import Aluno
from financeiro.models import PlanoMensalidade, ContratoAluno
from django.test import Client
from django.urls import reverse
import json

User = get_user_model()

def testar_ajax_valor():
    """Testa a funcionalidade AJAX de obter valor do contrato."""
    
    # Buscar ou criar um usuário de teste
    try:
        user = User.objects.get(username='admin')
        print(f"✓ Usuário admin encontrado: {user.email}")
    except User.DoesNotExist:
        print("✗ Usuário admin não encontrado")
        return
    
    # Buscar um aluno com contrato
    aluno = Aluno.objects.filter(personal_trainer=user).first()
    if not aluno:
        print("✗ Nenhum aluno encontrado para este usuário")
        return
    
    print(f"✓ Aluno encontrado: {aluno.nome}")
    
    # Verificar se o aluno tem contrato
    try:
        contrato = ContratoAluno.objects.get(aluno=aluno, ativo=True)
        print(f"✓ Contrato encontrado: {contrato.plano_mensalidade.nome} - R$ {contrato.valor_mensalidade}")
    except ContratoAluno.DoesNotExist:
        print("✗ Aluno não possui contrato ativo")
        return
    
    # Criar cliente de teste
    client = Client()
    
    # Fazer login
    client.force_login(user)
    
    # Testar a view AJAX
    url = reverse('financeiro:obter_valor_contrato')
    response = client.get(url, {'aluno_id': aluno.id})
    
    print(f"✓ Status da resposta: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Dados retornados:")
        print(f"  - Valor: R$ {data.get('valor', 'N/A')}")
        print(f"  - Plano: {data.get('plano', 'N/A')}")
        print(f"  - Dia vencimento: {data.get('dia_vencimento', 'N/A')}")
        
        # Verificar se os dados estão corretos
        if data.get('valor') == str(contrato.valor_mensalidade):
            print("✓ Valor correto!")
        else:
            print("✗ Valor incorreto!")
            
        if data.get('plano') == contrato.plano_mensalidade.nome:
            print("✓ Plano correto!")
        else:
            print("✗ Plano incorreto!")
            
        if data.get('dia_vencimento') == contrato.dia_vencimento:
            print("✓ Dia de vencimento correto!")
        else:
            print("✗ Dia de vencimento incorreto!")
            
    else:
        print(f"✗ Erro na requisição: {response.content}")
    
    print("\n=== Teste concluído ===")

if __name__ == '__main__':
    testar_ajax_valor()
