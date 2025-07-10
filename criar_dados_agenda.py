#!/usr/bin/env python
"""
Script para criar dados de teste para a agenda de aulas.
"""
import os
import sys
import django
from datetime import datetime, timedelta, time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from django.contrib.auth import get_user_model
from alunos.models import Aluno
from frequencia.models import AgendaAula

User = get_user_model()

def criar_dados_agenda():
    """
    Cria dados de teste para a agenda de aulas.
    """
    try:
        # Buscar um personal trainer (qualquer usuário ativo)
        personal = User.objects.filter(is_active=True).first()
        if not personal:
            print("❌ Nenhum usuário ativo encontrado")
            return
        
        print(f"✅ Personal trainer encontrado: {personal.nome_completo}")
        
        # Buscar alguns alunos
        alunos = Aluno.objects.filter(personal_trainer=personal)[:3]
        if not alunos:
            print("❌ Nenhum aluno encontrado")
            return
        
        print(f"✅ {len(alunos)} alunos encontrados")
        
        # Criar agendamentos com diferentes status
        hoje = datetime.now().date()
        status_list = ['agendado', 'confirmado', 'realizado', 'cancelado', 'remarcado']
        
        # Limpar agendamentos existentes
        AgendaAula.objects.filter(aluno__personal_trainer=personal).delete()
        print("✅ Agendamentos anteriores removidos")
        
        agendamentos_criados = 0
        
        for i, aluno in enumerate(alunos):
            for j, status in enumerate(status_list):
                data_aula = hoje + timedelta(days=j-2)  # Alguns no passado, alguns no futuro
                
                agenda = AgendaAula.objects.create(
                    aluno=aluno,
                    data_aula=data_aula,
                    horario_inicio=time(8 + j, 0),
                    horario_fim=time(9 + j, 0),
                    status=status,
                    tipo_treino=f"Treino {chr(65+j)}",
                    observacoes=f"Aula de teste com status {status}"
                )
                agendamentos_criados += 1
                print(f"✅ Criado agendamento: {aluno.nome} - {data_aula} - {status}")
        
        print(f"\n✅ {agendamentos_criados} agendamentos criados com sucesso!")
        
        # Mostrar resumo
        print("\n📊 Resumo por status:")
        for status_value, status_label in AgendaAula.STATUS_CHOICES:
            count = AgendaAula.objects.filter(
                aluno__personal_trainer=personal,
                status=status_value
            ).count()
            print(f"  {status_label}: {count}")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    criar_dados_agenda()
