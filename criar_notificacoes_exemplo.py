"""
Script para criar notificações de exemplo para teste.
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
sys.path.append('/Users/romariorodrigues/DEV/FormaFit')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from accounts.models import User
from alunos.models import Aluno
from notificacoes.models import Notificacao, TipoNotificacao

def criar_notificacoes_exemplo():
    """Criar algumas notificações de exemplo."""
    
    # Buscar o primeiro personal trainer
    try:
        personal = User.objects.filter(is_superuser=True).first()
        if not personal:
            print("❌ Nenhum personal trainer encontrado. Crie um superusuário primeiro.")
            return
        
        print(f"✓ Personal encontrado: {personal.email}")
        
        # Buscar tipos de notificação
        tipo_treino = TipoNotificacao.objects.get(nome='Lembrete de Treino')
        tipo_cobranca = TipoNotificacao.objects.get(nome='Cobrança de Mensalidade')
        tipo_motivacional = TipoNotificacao.objects.get(nome='Mensagem Motivacional')
        
        # Buscar um aluno (se existir)
        aluno = Aluno.objects.filter(personal_trainer=personal).first()
        
        # Criar notificações
        notificacoes = [
            {
                'titulo': '🏋️ Lembrete: Treino hoje às 14h',
                'mensagem': 'Olá! Você tem treino agendado hoje às 14:00. Não se esqueça de trazer toalha e garrafa de água. Nos vemos em breve! 💪',
                'tipo_notificacao': tipo_treino,
                'aluno': aluno,
                'status': 'enviada',
                'enviado_whatsapp': True,
                'data_criacao': datetime.now() - timedelta(hours=2)
            },
            {
                'titulo': '💰 Lembrete: Mensalidade vence amanhã',
                'mensagem': 'Sua mensalidade vence amanhã (31/12). Valor: R$ 150,00. Para manter seu treino em dia, efetue o pagamento até a data de vencimento.',
                'tipo_notificacao': tipo_cobranca,
                'aluno': aluno,
                'status': 'enviada',
                'enviado_whatsapp': True,
                'data_criacao': datetime.now() - timedelta(hours=1)
            },
            {
                'titulo': '🎯 Você está indo muito bem!',
                'mensagem': 'Parabéns pelo seu empenho nos treinos esta semana! Sua dedicação é inspiradora. Continue assim que os resultados virão! 🌟',
                'tipo_notificacao': tipo_motivacional,
                'aluno': aluno,
                'status': 'enviada',
                'enviado_sistema': True,
                'data_criacao': datetime.now() - timedelta(minutes=30)
            },
            {
                'titulo': '📊 Novo relatório disponível',
                'mensagem': 'Seu relatório mensal de evolução está pronto! Acesse o sistema para ver seu progresso e conquistas do mês.',
                'tipo_notificacao': tipo_motivacional,
                'aluno': aluno,
                'status': 'pendente',
                'enviado_email': False,
                'enviado_sistema': False,
                'data_criacao': datetime.now() - timedelta(minutes=10)
            }
        ]
        
        for notif_data in notificacoes:
            notificacao = Notificacao.objects.create(
                personal_trainer=personal,
                **notif_data
            )
            print(f'✓ Notificação criada: {notificacao.titulo}')
        
        print(f'\n✅ {len(notificacoes)} notificações de exemplo criadas!')
        
    except Exception as e:
        print(f"❌ Erro ao criar notificações: {str(e)}")

if __name__ == '__main__':
    print('Criando notificações de exemplo...\n')
    criar_notificacoes_exemplo()
    print('\nAcesse /notificacoes/ para ver as notificações criadas.')
