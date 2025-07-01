"""
Context processors para disponibilizar dados globalmente nos templates.
"""
from notificacoes.models import Notificacao


def notificacoes_context(request):
    """
    Adiciona informações de notificações a todos os templates.
    """
    if request.user.is_authenticated:
        notificacoes_nao_lidas = Notificacao.objects.filter(
            personal_trainer=request.user,
            status='enviada'
        ).count()
        
        notificacoes_recentes = Notificacao.objects.filter(
            personal_trainer=request.user,
            status='enviada'
        ).order_by('-data_criacao')[:5]
        
        return {
            'notificacoes_nao_lidas': notificacoes_nao_lidas,
            'notificacoes_recentes': notificacoes_recentes
        }
    
    return {
        'notificacoes_nao_lidas': 0,
        'notificacoes_recentes': []
    }
