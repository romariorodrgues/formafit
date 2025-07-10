#!/usr/bin/env python
"""
Script para testar o formulário de fatura completo.
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
from financeiro.models import PlanoMensalidade, ContratoAluno, Fatura
from financeiro.forms import FaturaForm
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

def testar_formulario_fatura():
    """Testa o formulário de fatura com dados completos."""
    
    # Buscar usuário admin
    try:
        user = User.objects.get(username='admin')
        print(f"✓ Usuário admin encontrado: {user.email}")
    except User.DoesNotExist:
        print("✗ Usuário admin não encontrado")
        return
    
    # Buscar aluno com contrato
    aluno = Aluno.objects.filter(personal_trainer=user).first()
    if not aluno:
        print("✗ Nenhum aluno encontrado")
        return
    
    print(f"✓ Aluno encontrado: {aluno.nome}")
    
    # Testar o formulário
    form_data = {
        'aluno': aluno.id,
        'mes_referencia': 7,
        'ano_referencia': 2025,
        'valor_original': '150.00',
        'desconto': '10.00',
        'acrescimo': '5.00',
        'data_vencimento': '2025-07-05',
        'observacoes': 'Fatura de teste'
    }
    
    print("✓ Dados do formulário:")
    for key, value in form_data.items():
        print(f"  - {key}: {value}")
    
    # Criar formulário
    form = FaturaForm(data=form_data, user=user)
    
    print(f"\n✓ Formulário válido: {form.is_valid()}")
    
    if form.is_valid():
        print("✓ Formulário validado com sucesso!")
        
        # Testar salvamento (não salvar de verdade)
        fatura = form.save(commit=False)
        print(f"✓ Fatura criada (não salva):")
        print(f"  - Aluno: {fatura.aluno.nome}")
        print(f"  - Valor Original: R$ {fatura.valor_original}")
        print(f"  - Desconto: R$ {fatura.desconto}")
        print(f"  - Acréscimo: R$ {fatura.acrescimo}")
        print(f"  - Valor Final: R$ {fatura.valor_final}")
        print(f"  - Data Vencimento: {fatura.data_vencimento}")
        print(f"  - Observações: {fatura.observacoes}")
        
        # Verificar se o contrato seria associado
        try:
            contrato = ContratoAluno.objects.get(aluno=fatura.aluno, ativo=True)
            print(f"✓ Contrato associado: {contrato.plano_mensalidade.nome}")
        except ContratoAluno.DoesNotExist:
            print("✗ Nenhum contrato ativo encontrado")
        
    else:
        print("✗ Formulário inválido!")
        print("Erros:")
        for field, errors in form.errors.items():
            print(f"  - {field}: {errors}")
    
    print("\n=== Teste do formulário concluído ===")

if __name__ == '__main__':
    testar_formulario_fatura()
