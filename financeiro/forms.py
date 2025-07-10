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
        labels = {
            'nome': 'Nome do Plano',
            'descricao': 'Descrição',
            'valor': 'Valor Mensal (R$)',
            'aulas_incluidas': 'Aulas Incluídas',
            'ativo': 'Plano Ativo'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Ex: Plano Básico, Plano Premium'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva os benefícios e características do plano...'
            }),
            'valor': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'aulas_incluidas': forms.NumberInput(attrs={
                'min': '1',
                'placeholder': 'Ex: 8 aulas por mês'
            }),
        }
    
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor and valor <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero.')
        return valor
    
    def clean_aulas_incluidas(self):
        aulas = self.cleaned_data.get('aulas_incluidas')
        if aulas and aulas <= 0:
            raise forms.ValidationError('Deve ter pelo menos 1 aula incluída.')
        return aulas


class ContratoAlunoForm(forms.ModelForm):
    """
    Formulário para contratos de alunos.
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filtrar apenas alunos do personal trainer logado que ainda não têm contrato ativo
            alunos_sem_contrato = Aluno.objects.filter(
                personal_trainer=user
            ).exclude(
                contrato__ativo=True
            )
            self.fields['aluno'].queryset = alunos_sem_contrato
            
            # Filtrar apenas planos ativos
            self.fields['plano_mensalidade'].queryset = PlanoMensalidade.objects.filter(ativo=True)
            
            if not alunos_sem_contrato.exists():
                self.fields['aluno'].choices = [('', 'Todos os alunos já possuem contratos ativos')]
        
        # Configurar valores padrão
        if not self.instance.pk:
            from django.utils import timezone
            self.fields['data_inicio'].initial = timezone.now().date()
            self.fields['dia_vencimento'].initial = 5
    
    class Meta:
        model = ContratoAluno
        fields = ['aluno', 'plano_mensalidade', 'valor_personalizado', 'dia_vencimento', 'data_inicio', 'observacoes']
        labels = {
            'aluno': 'Aluno',
            'plano_mensalidade': 'Plano de Mensalidade',
            'valor_personalizado': 'Valor Personalizado (R$)',
            'dia_vencimento': 'Dia do Vencimento',
            'data_inicio': 'Data de Início',
            'observacoes': 'Observações'
        }
        widgets = {
            'aluno': forms.Select(attrs={
                'placeholder': 'Selecione o aluno...'
            }),
            'plano_mensalidade': forms.Select(attrs={
                'placeholder': 'Selecione o plano...'
            }),
            'valor_personalizado': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'placeholder': 'Deixe vazio para usar valor do plano'
            }),
            'dia_vencimento': forms.NumberInput(attrs={
                'min': '1',
                'max': '31',
                'placeholder': 'Ex: 5'
            }),
            'data_inicio': forms.DateInput(attrs={
                'type': 'date'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Observações sobre o contrato...'
            })
        }
    
    def clean_dia_vencimento(self):
        dia = self.cleaned_data.get('dia_vencimento')
        if dia and (dia < 1 or dia > 31):
            raise forms.ValidationError('O dia deve estar entre 1 e 31.')
        return dia
    
    def clean_valor_personalizado(self):
        valor = self.cleaned_data.get('valor_personalizado')
        if valor and valor <= 0:
            raise forms.ValidationError('O valor personalizado deve ser maior que zero.')
        return valor
    
    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        
        if aluno:
            # Verificar se o aluno já possui um contrato ativo
            existing = ContratoAluno.objects.filter(
                aluno=aluno,
                ativo=True
            )
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError(
                    f'{aluno.nome} já possui um contrato ativo.'
                )
        
        return cleaned_data


class FaturaForm(forms.ModelForm):
    """
    Formulário para faturas.
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filtrar apenas alunos do personal trainer logado que têm contratos ativos
            alunos_com_contrato = Aluno.objects.filter(
                personal_trainer=user,
                contrato__ativo=True
            ).distinct()
            self.fields['aluno'].queryset = alunos_com_contrato
            
            # Melhorar as opções do select com informações do contrato
            if alunos_com_contrato.exists():
                choices = [('', '--- Selecione um aluno ---')]
                for aluno in alunos_com_contrato:
                    try:
                        contrato = aluno.contrato
                        choice_text = f"{aluno.nome} - {contrato.plano_mensalidade.nome} (R$ {contrato.valor_mensalidade})"
                        choices.append((aluno.id, choice_text))
                    except ContratoAluno.DoesNotExist:
                        choices.append((aluno.id, f"{aluno.nome} - Sem contrato ativo"))
                
                self.fields['aluno'].choices = choices
            else:
                self.fields['aluno'].choices = [('', 'Nenhum aluno com contrato ativo encontrado')]
        
        # Configurar valores padrão
        if not self.instance.pk:  # Apenas para novos registros
            from django.utils import timezone
            hoje = timezone.now().date()
            self.fields['mes_referencia'].initial = hoje.month
            self.fields['ano_referencia'].initial = hoje.year
    
    class Meta:
        model = Fatura
        fields = ['aluno', 'mes_referencia', 'ano_referencia', 'valor_original', 'desconto', 'acrescimo', 'data_vencimento', 'observacoes']
        labels = {
            'aluno': 'Aluno/Contrato',
            'mes_referencia': 'Mês de Referência',
            'ano_referencia': 'Ano de Referência',
            'valor_original': 'Valor Original (R$)',
            'desconto': 'Desconto (R$)',
            'acrescimo': 'Acréscimo (R$)',
            'data_vencimento': 'Data de Vencimento',
            'observacoes': 'Observações'
        }
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Selecione o aluno...'
            }),
            'mes_referencia': forms.Select(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Selecione o mês...'
            }),
            'ano_referencia': forms.NumberInput(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'min': '2020',
                'max': '2030',
                'placeholder': 'Ex: 2025'
            }),
            'valor_original': forms.NumberInput(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'desconto': forms.NumberInput(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'step': '0.01',
                'min': '0',
                'value': '0.00',
                'placeholder': '0.00'
            }),
            'acrescimo': forms.NumberInput(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'step': '0.01',
                'min': '0',
                'value': '0.00',
                'placeholder': '0.00'
            }),
            'data_vencimento': forms.DateInput(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'type': 'date'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Observações sobre a fatura...'
            })
        }
    
    def clean_valor_original(self):
        valor = self.cleaned_data.get('valor_original')
        if valor and valor <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero.')
        return valor
    
    def clean(self):
        cleaned_data = super().clean()
        aluno = cleaned_data.get('aluno')
        mes = cleaned_data.get('mes_referencia')
        ano = cleaned_data.get('ano_referencia')
        
        if aluno and mes and ano:
            # Verificar se já existe uma fatura para este aluno no mesmo período
            existing = Fatura.objects.filter(
                aluno=aluno,
                mes_referencia=mes,
                ano_referencia=ano
            )
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise forms.ValidationError(
                    f'Já existe uma fatura para {aluno.nome} no período {mes}/{ano}.'
                )
        
        return cleaned_data


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
