"""
Formulários para gestão financeira.
"""
from django import forms
from decimal import Decimal
from .models import PlanoMensalidade, ContratoAluno, Fatura, Pagamento
from alunos.models import Aluno


class PlanoMensalidadeForm(forms.ModelForm):
    """
    Formulário para criação de planos de mensalidade.
    """
    class Meta:
        model = PlanoMensalidade
        fields = ['nome', 'descricao', 'valor', 'aulas_incluidas', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: Plano Básico'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Descrição do plano...'
            }),
            'valor': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': '0.00'
            }),
            'aulas_incluidas': forms.NumberInput(attrs={
                'min': '1',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 8'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
            })
        }


class ContratoAlunoForm(forms.ModelForm):
    """
    Formulário para contratos de alunos.
    """
    class Meta:
        model = ContratoAluno
        fields = ['aluno', 'plano_mensalidade', 'valor_personalizado', 'dia_vencimento', 'data_inicio', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'plano_mensalidade': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'valor_personalizado': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Deixe vazio para usar valor do plano'
            }),
            'dia_vencimento': forms.NumberInput(attrs={
                'min': '1',
                'max': '31',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'data_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre o contrato...'
            })
        }


class FaturaForm(forms.ModelForm):
    """
    Formulário para faturas.
    """
    class Meta:
        model = Fatura
        fields = ['aluno', 'mes_referencia', 'ano_referencia', 'valor_original', 'desconto', 'acrescimo', 'data_vencimento', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'mes_referencia': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'ano_referencia': forms.NumberInput(attrs={
                'min': '2020',
                'max': '2030',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'valor_original': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'desconto': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'value': '0.00'
            }),
            'acrescimo': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'value': '0.00'
            }),
            'data_vencimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre a fatura...'
            })
        }


class PagamentoForm(forms.ModelForm):
    """
    Formulário para registrar pagamentos.
    """
    class Meta:
        model = Pagamento
        fields = ['data_pagamento', 'valor_pago', 'forma_pagamento', 'observacoes', 'comprovante']
        widgets = {
            'data_pagamento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'valor_pago': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'forma_pagamento': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 2,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre o pagamento...'
            }),
            'comprovante': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            })
        }


class FiltroFinanceiroForm(forms.Form):
    """
    Formulário para filtrar dados financeiros.
    """
    MESES_CHOICES = [('', 'Todos os meses')] + [(i, f"{i:02d}") for i in range(1, 13)]
    ANOS_CHOICES = [('', 'Todos os anos')] + [(i, str(i)) for i in range(2020, 2030)]
    STATUS_CHOICES = [('', 'Todos os status')] + Fatura.STATUS_CHOICES
    
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        required=False,
        empty_label="Todos os alunos",
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    mes = forms.ChoiceField(
        choices=MESES_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    ano = forms.ChoiceField(
        choices=ANOS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas alunos do personal trainer logado
        self.fields['aluno'].queryset = Aluno.objects.filter(
            personal_trainer=user,
            ativo=True
        )


class GerarFaturaForm(forms.Form):
    """
    Formulário para gerar faturas em lote.
    """
    mes_referencia = forms.ChoiceField(
        choices=[(i, f"{i:02d}") for i in range(1, 13)],
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    ano_referencia = forms.IntegerField(
        min_value=2020,
        max_value=2030,
        widget=forms.NumberInput(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    alunos_selecionados = forms.ModelMultipleChoiceField(
        queryset=Aluno.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
        }),
        required=False
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas alunos do personal trainer logado que têm contrato
        self.fields['alunos_selecionados'].queryset = Aluno.objects.filter(
            personal_trainer=user,
            ativo=True,
            contrato__isnull=False
        )
