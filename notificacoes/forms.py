"""
Formulários para sistema de notificações.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Notificacao, TipoNotificacao, NotificacaoAutomatica, 
    ConfiguracaoNotificacao
)
from alunos.models import Aluno


class NotificacaoForm(forms.ModelForm):
    """Formulário para criar notificações manuais."""
    
    enviar_agora = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Marque para enviar a notificação imediatamente"
    )
    
    class Meta:
        model = Notificacao
        fields = [
            'tipo_notificacao', 'aluno', 'titulo', 'mensagem', 
            'prioridade', 'data_agendamento'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Título da notificação'
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Mensagem da notificação'
            }),
            'tipo_notificacao': forms.Select(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'aluno': forms.Select(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'prioridade': forms.Select(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'data_agendamento': forms.DateTimeInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'tipo_notificacao': 'Tipo de Notificação',
            'aluno': 'Aluno (opcional)',
            'titulo': 'Título',
            'mensagem': 'Mensagem',
            'prioridade': 'Prioridade',
            'data_agendamento': 'Data de Agendamento',
        }
        help_texts = {
            'aluno': 'Deixe em branco para notificação geral',
            'data_agendamento': 'Data e hora para envio da notificação',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filtrar alunos do personal trainer
            self.fields['aluno'].queryset = Aluno.objects.filter(
                personal_trainer=user, 
                ativo=True
            )
            # Adicionar opção vazia
            self.fields['aluno'].empty_label = "Notificação geral (sem aluno específico)"
        
        # Filtrar tipos ativos
        self.fields['tipo_notificacao'].queryset = TipoNotificacao.objects.filter(ativo=True)


class TipoNotificacaoForm(forms.ModelForm):
    """Formulário para tipos de notificação."""
    
    class Meta:
        model = TipoNotificacao
        fields = [
            'nome', 'descricao', 'template_titulo', 'template_mensagem',
            'enviar_email', 'enviar_whatsapp', 'enviar_sistema', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Nome do tipo de notificação'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Descrição opcional do tipo'
            }),
            'template_titulo': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Template do título (ex: Lembrete: {{aluno.nome}})'
            }),
            'template_mensagem': forms.Textarea(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Template da mensagem'
            }),
        }
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'template_titulo': 'Template do Título',
            'template_mensagem': 'Template da Mensagem',
            'enviar_email': 'Enviar por Email',
            'enviar_whatsapp': 'Enviar por WhatsApp',
            'enviar_sistema': 'Notificação do Sistema',
            'ativo': 'Ativo',
        }
        help_texts = {
            'template_titulo': 'Use {{aluno.nome}}, {{personal_trainer.nome}}, etc.',
            'template_mensagem': 'Use variáveis como {{aluno.nome}}, {{valor}}, {{data}}, etc.',
        }


class ConfiguracaoNotificacaoForm(forms.ModelForm):
    """Formulário para configurações de notificação do aluno."""
    
    class Meta:
        model = ConfiguracaoNotificacao
        fields = [
            'receber_email', 'receber_whatsapp', 'receber_lembrete_pagamento',
            'receber_lembrete_treino', 'receber_relatorio_progresso',
            'horario_preferencial', 'dias_antecedencia_pagamento',
            'email_alternativo', 'telefone_alternativo'
        ]
        widgets = {
            'horario_preferencial': forms.TimeInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'type': 'time'
            }),
            'dias_antecedencia_pagamento': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'min': 1,
                'max': 30
            }),
            'email_alternativo': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'email@exemplo.com'
            }),
            'telefone_alternativo': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'placeholder': '(11) 99999-9999'
            }),
        }
        labels = {
            'receber_email': 'Receber Notificações por Email',
            'receber_whatsapp': 'Receber Notificações por WhatsApp',
            'receber_lembrete_pagamento': 'Lembretes de Pagamento',
            'receber_lembrete_treino': 'Lembretes de Treino',
            'receber_relatorio_progresso': 'Relatórios de Progresso',
            'horario_preferencial': 'Horário Preferencial',
            'dias_antecedencia_pagamento': 'Dias de Antecedência para Pagamento',
            'email_alternativo': 'Email Alternativo',
            'telefone_alternativo': 'Telefone Alternativo',
        }
        help_texts = {
            'horario_preferencial': 'Horário preferencial para receber notificações',
            'dias_antecedencia_pagamento': 'Quantos dias antes do vencimento enviar lembrete',
            'email_alternativo': 'Email adicional para receber notificações',
            'telefone_alternativo': 'Telefone adicional para WhatsApp',
        }


class FiltroNotificacaoForm(forms.Form):
    """Formulário para filtrar notificações."""
    
    STATUS_CHOICES = [
        ('', 'Todos os Status'),
        ('pendente', 'Pendente'),
        ('enviada', 'Enviada'),
        ('lida', 'Lida'),
        ('erro', 'Erro no Envio'),
        ('cancelada', 'Cancelada'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        })
    )
    
    tipo = forms.ModelChoiceField(
        queryset=TipoNotificacao.objects.filter(ativo=True),
        required=False,
        empty_label="Todos os Tipos",
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        })
    )
    
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'type': 'date'
        }),
        label='Data Início'
    )
    
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'type': 'date'
        }),
        label='Data Fim'
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Adicionar campo de aluno
            self.fields['aluno'] = forms.ModelChoiceField(
                queryset=Aluno.objects.filter(personal_trainer=user, ativo=True),
                required=False,
                empty_label="Todos os Alunos",
                widget=forms.Select(attrs={
                    'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
                })
            )


class TesteWhatsAppForm(forms.Form):
    """Formulário para teste de WhatsApp."""
    
    telefone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': '(11) 99999-9999'
        }),
        label='Telefone'
    )
    
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 4,
            'placeholder': 'Mensagem de teste'
        }),
        label='Mensagem'
    )
    
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        # Remover caracteres não numéricos
        telefone_clean = ''.join(filter(str.isdigit, telefone))
        
        if len(telefone_clean) < 10:
            raise ValidationError('Telefone deve ter pelo menos 10 dígitos')
        
        return telefone_clean
