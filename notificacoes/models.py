"""
Modelos para sistema de notificações.
"""
from django.db import models
from django.utils import timezone
from django.conf import settings
from alunos.models import Aluno


class TipoNotificacao(models.Model):
    """
    Tipos de notificações disponíveis no sistema.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    cor = models.CharField(max_length=7, default='#6B7280', help_text="Cor hexadecimal para identificação visual")
    template_titulo = models.CharField(max_length=200, help_text="Template do título da notificação", blank=True)
    template_mensagem = models.TextField(help_text="Template da mensagem da notificação", blank=True)
    ativo = models.BooleanField(default=True)
    
    # Configurações de envio
    enviar_email = models.BooleanField(default=False)
    enviar_whatsapp = models.BooleanField(default=False)
    enviar_sistema = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tipo de Notificação'
        verbose_name_plural = 'Tipos de Notificação'
    
    def __str__(self):
        return self.nome


class Notificacao(models.Model):
    """
    Notificações do sistema.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('enviada', 'Enviada'),
        ('lida', 'Lida'),
        ('erro', 'Erro no Envio'),
        ('cancelada', 'Cancelada'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    tipo_notificacao = models.ForeignKey(TipoNotificacao, on_delete=models.CASCADE, related_name='notificacoes')
    personal_trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificacoes_enviadas')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notificacoes', blank=True, null=True)
    
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='normal')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    
    # Datas
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_agendamento = models.DateTimeField(default=timezone.now)
    data_envio = models.DateTimeField(blank=True, null=True)
    data_leitura = models.DateTimeField(blank=True, null=True)
    
    # Resultados do envio
    enviado_email = models.BooleanField(default=False)
    enviado_whatsapp = models.BooleanField(default=False)
    enviado_sistema = models.BooleanField(default=False)
    
    erro_envio = models.TextField(blank=True, help_text="Detalhes do erro, se houver")
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-data_criacao']
    
    def __str__(self):
        destino = self.aluno.nome if self.aluno else "Sistema"
        return f"{self.titulo} - {destino} - {self.get_status_display()}"
    
    def marcar_como_lida(self):
        """Marca a notificação como lida."""
        if self.status == 'enviada':
            self.status = 'lida'
            self.data_leitura = timezone.now()
            self.save()


class NotificacaoAutomatica(models.Model):
    """
    Configurações para notificações automáticas.
    """
    TRIGGER_CHOICES = [
        ('pagamento_vencido', 'Pagamento Vencido'),
        ('pagamento_vence_hoje', 'Pagamento Vence Hoje'),
        ('pagamento_vence_amanha', 'Pagamento Vence Amanhã'),
        ('pagamento_vence_3_dias', 'Pagamento Vence em 3 Dias'),
        ('aniversario_aluno', 'Aniversário do Aluno'),
        ('novo_relatorio_disponivel', 'Novo Relatório Disponível'),
        ('treino_agendado', 'Lembrete de Treino'),
        ('falta_frequente', 'Aluno com Muitas Faltas'),
    ]
    
    nome = models.CharField(max_length=200)
    trigger = models.CharField(max_length=30, choices=TRIGGER_CHOICES, unique=True)
    tipo_notificacao = models.ForeignKey(TipoNotificacao, on_delete=models.CASCADE)
    ativa = models.BooleanField(default=True)
    
    # Configurações de tempo
    antecedencia_dias = models.IntegerField(default=0, help_text="Dias de antecedência para envio")
    horario_envio = models.TimeField(default=timezone.now().time(), help_text="Horário preferencial para envio")
    
    # Filtros
    apenas_alunos_ativos = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Notificação Automática'
        verbose_name_plural = 'Notificações Automáticas'
    
    def __str__(self):
        return f"{self.nome} - {self.get_trigger_display()}"


class LogEnvioWhatsApp(models.Model):
    """
    Log de envios via WhatsApp usando a API do ChatPro.
    """
    STATUS_CHOICES = [
        ('sucesso', 'Sucesso'),
        ('erro', 'Erro'),
        ('pendente', 'Pendente'),
    ]
    
    notificacao = models.ForeignKey(Notificacao, on_delete=models.CASCADE, related_name='logs_whatsapp')
    telefone_destino = models.CharField(max_length=20)
    mensagem_enviada = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    response_api = models.JSONField(blank=True, null=True, help_text="Resposta da API do ChatPro")
    tentativas = models.IntegerField(default=1)
    data_envio = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log WhatsApp'
        verbose_name_plural = 'Logs WhatsApp'
        ordering = ['-data_envio']
    
    def __str__(self):
        return f"WhatsApp para {self.telefone_destino} - {self.get_status_display()}"


class ConfiguracaoNotificacao(models.Model):
    """
    Configurações personalizadas de notificação por aluno.
    """
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, related_name='config_notificacao')
    
    # Preferências de recebimento
    receber_email = models.BooleanField(default=True)
    receber_whatsapp = models.BooleanField(default=True)
    receber_lembrete_pagamento = models.BooleanField(default=True)
    receber_lembrete_treino = models.BooleanField(default=True)
    receber_relatorio_progresso = models.BooleanField(default=True)
    
    # Configurações de horário
    horario_preferencial = models.TimeField(default=timezone.now().time())
    dias_antecedencia_pagamento = models.IntegerField(default=3)
    
    # Contatos alternativos
    email_alternativo = models.EmailField(blank=True)
    telefone_alternativo = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Configuração de Notificação'
        verbose_name_plural = 'Configurações de Notificação'
    
    def __str__(self):
        return f"Configurações - {self.aluno.nome}"
