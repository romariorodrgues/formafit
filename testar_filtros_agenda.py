#!/usr/bin/env python
"""
Script para testar os filtros da agenda.
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from django.contrib.auth import get_user_model
from alunos.models import Aluno
from frequencia.models import AgendaAula

User = get_user_model()

def testar_filtros():
    """
    Testa os filtros da agenda.
    """
    try:
        # Buscar um personal trainer
        personal = User.objects.filter(is_active=True).first()
        if not personal:
            print("❌ Nenhum usuário ativo encontrado")
            return
        
        print(f"✅ Personal trainer encontrado: {personal.nome_completo}")
        
        # Testar filtros por status
        print("\n🔍 Testando filtros por status:")
        
        for status_value, status_label in AgendaAula.STATUS_CHOICES:
            count = AgendaAula.objects.filter(
                aluno__personal_trainer=personal,
                status=status_value
            ).count()
            print(f"  {status_label} ({status_value}): {count} agendamentos")
            
            # Mostrar alguns exemplos
            if count > 0:
                agendamentos = AgendaAula.objects.filter(
                    aluno__personal_trainer=personal,
                    status=status_value
                )[:2]
                for agenda in agendamentos:
                    print(f"    - {agenda.aluno.nome} | {agenda.data_aula} | {agenda.horario_inicio} | {agenda.get_status_display()}")
        
        # Testar filtro por data
        print("\n📅 Testando filtro por data:")
        hoje = datetime.now().date()
        
        agendamentos_hoje = AgendaAula.objects.filter(
            aluno__personal_trainer=personal,
            data_aula=hoje
        )
        print(f"  Agendamentos para hoje ({hoje}): {agendamentos_hoje.count()}")
        
        for agenda in agendamentos_hoje:
            print(f"    - {agenda.aluno.nome} | {agenda.horario_inicio} | {agenda.get_status_display()}")
        
        # Testar combinação de filtros
        print("\n🎯 Testando combinação de filtros:")
        agendamentos_hoje_agendado = AgendaAula.objects.filter(
            aluno__personal_trainer=personal,
            data_aula=hoje,
            status='agendado'
        )
        print(f"  Agendamentos hoje com status 'agendado': {agendamentos_hoje_agendado.count()}")
        
    except Exception as e:
        print(f"❌ Erro ao testar filtros: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    testar_filtros()
