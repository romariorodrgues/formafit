"""
Formulários para o sistema de relatórios.
"""
from django import forms
from django.utils import timezone
from datetime import datetime, timedelta
from .models import RelatorioProgresso, TipoRelatorio
from alunos.models import Aluno


class GerarRelatorioForm(forms.ModelForm):
    """Formulário para gerar relatório de progresso."""
    
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        label='Aluno'
    )
    
    tipo_relatorio = forms.ModelChoiceField(
        queryset=TipoRelatorio.objects.filter(ativo=True),
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        label='Tipo de Relatório'
    )
    
    periodo = forms.ChoiceField(
        choices=RelatorioProgresso.PERIODO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'onchange': 'updateDateFields()'
        }),
        label='Período'
    )
    
    data_inicio = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        label='Data de Início'
    )
    
    data_fim = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        label='Data de Fim'
    )
    
    titulo = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Ex: Relatório Mensal de Janeiro 2025'
        }),
        label='Título do Relatório'
    )
    
    observacoes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'rows': 4,
            'placeholder': 'Observações adicionais sobre o período...'
        }),
        label='Observações'
    )
    
    class Meta:
        model = RelatorioProgresso
        fields = ['aluno', 'tipo_relatorio', 'periodo', 'data_inicio', 'data_fim', 'titulo', 'observacoes']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filtrar apenas alunos do personal trainer logado
            self.fields['aluno'].queryset = Aluno.objects.filter(personal_trainer=user)
        
        # Definir datas padrão
        hoje = timezone.now().date()
        self.fields['data_fim'].initial = hoje
        self.fields['data_inicio'].initial = hoje - timedelta(days=30)
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        
        if data_inicio and data_fim:
            if data_inicio > data_fim:
                raise forms.ValidationError('A data de início deve ser anterior à data de fim.')
            
            if data_fim > timezone.now().date():
                raise forms.ValidationError('A data de fim não pode ser futura.')
            
            # Verificar se o período não é muito longo (máximo 1 ano)
            if (data_fim - data_inicio).days > 365:
                raise forms.ValidationError('O período do relatório não pode ser superior a 1 ano.')
        
        return cleaned_data


class FiltroRelatoriosForm(forms.Form):
    """Formulário para filtrar relatórios."""
    
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        required=False,
        empty_label='Todos os alunos',
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
    periodo = forms.ChoiceField(
        choices=[('', 'Todos os períodos')] + RelatorioProgresso.PERIODO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'Todos os status')] + RelatorioProgresso.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        label='Data Início'
    )
    
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        label='Data Fim'
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['aluno'].queryset = Aluno.objects.filter(personal_trainer=user)
