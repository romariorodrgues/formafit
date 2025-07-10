#!/usr/bin/env python
"""
Script para criar dados financeiros de teste.
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from django.contrib.auth import get_user_model
from alunos.models import Aluno
from financeiro.models import PlanoMensalidade, ContratoAluno

User = get_user_model()

def criar_dados_financeiros():
    """
    Cria dados financeiros de teste.
    """
    try:
        # Buscar usuário
        user = User.objects.first()
        if not user:
            print("❌ Nenhum usuário encontrado")
            return
        
        print(f"✅ Usuário encontrado: {user.username}")
        
        # Criar planos de mensalidade
        planos = [
            {
                'nome': 'Plano Básico',
                'descricao': 'Plano com 8 aulas por mês. Ideal para iniciantes.',
                'valor': Decimal('150.00'),
                'aulas_incluidas': 8
            },
            {
                'nome': 'Plano Intermediário',
                'descricao': 'Plano com 12 aulas por mês. Perfeito para evolução contínua.',
                'valor': Decimal('200.00'),
                'aulas_incluidas': 12
            },
            {
                'nome': 'Plano Premium',
                'descricao': 'Plano com 16 aulas por mês. Para máximos resultados.',
                'valor': Decimal('280.00'),
                'aulas_incluidas': 16
            }
        ]
        
        planos_criados = []
        for plano_data in planos:
            plano, created = PlanoMensalidade.objects.get_or_create(
                nome=plano_data['nome'],
                defaults=plano_data
            )
            if created:
                print(f"✅ Plano criado: {plano.nome} - R$ {plano.valor}")
            else:
                print(f"ℹ️  Plano já existe: {plano.nome}")
            planos_criados.append(plano)
        
        # Buscar alunos
        alunos = Aluno.objects.filter(personal_trainer=user)
        if not alunos.exists():
            print("❌ Nenhum aluno encontrado")
            return
        
        print(f"✅ {alunos.count()} alunos encontrados")
        
        # Criar contratos para os alunos
        contratos_criados = 0
        for i, aluno in enumerate(alunos):
            # Verificar se já tem contrato
            if ContratoAluno.objects.filter(aluno=aluno).exists():
                print(f"ℹ️  {aluno.nome} já tem contrato")
                continue
            
            # Atribuir planos diferentes para cada aluno
            plano = planos_criados[i % len(planos_criados)]
            
            contrato = ContratoAluno.objects.create(
                aluno=aluno,
                plano_mensalidade=plano,
                dia_vencimento=5,
                ativo=True,
                observacoes=f"Contrato criado automaticamente para teste"
            )
            contratos_criados += 1
            print(f"✅ Contrato criado: {aluno.nome} -> {plano.nome}")
        
        print(f"\\n✅ {len(planos_criados)} planos de mensalidade criados")
        print(f"✅ {contratos_criados} contratos criados")
        
        # Verificar resultado final
        alunos_com_contrato = Aluno.objects.filter(
            personal_trainer=user,
            contrato__ativo=True
        ).distinct()
        print(f"\\n📊 Resultado final:")
        print(f"   Alunos com contratos ativos: {alunos_com_contrato.count()}")
        for aluno in alunos_com_contrato:
            print(f"   - {aluno.nome}: {aluno.contrato.plano_mensalidade.nome} (R$ {aluno.contrato.valor_mensalidade})")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    criar_dados_financeiros()
