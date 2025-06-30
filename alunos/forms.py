"""
Formulários para gerenciamento de alunos.
"""
from django import forms
from django.core.validators import RegexValidator
from .models import Aluno, MedidasCorporais, FotoProgresso


class AlunoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de alunos.
    """
    telefone = forms.CharField(
        validators=[RegexValidator(
            regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
            message='Digite o telefone no formato: (11) 99999-9999'
        )],
        widget=forms.TextInput(attrs={
            'placeholder': '(11) 99999-9999',
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    class Meta:
        model = Aluno
        fields = [
            'nome', 'email', 'telefone', 'data_nascimento',
            'sexo', 'altura', 'peso_inicial', 'objetivo',
            'observacoes', 'endereco', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nome completo do aluno'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'email@exemplo.com'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'sexo': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'altura': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0.5',
                'max': '2.5',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 1.75'
            }),
            'peso_inicial': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '20',
                'max': '300',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 70.5'
            }),
            'objetivo': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Descreva os objetivos do aluno...'
            }),
            'nivel_atividade': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'endereco': forms.Textarea(attrs={
                'rows': 2,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Endereço completo...'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações gerais, histórico médico, restrições...'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
            })
        }


class MedidasCorporaisForm(forms.ModelForm):
    """
    Formulário para registro de medidas corporais.
    """
    class Meta:
        model = MedidasCorporais
        fields = [
            'peso', 'percentual_gordura', 'pescoco', 'torax', 
            'cintura', 'quadril', 'braco_direito', 'braco_esquerdo',
            'coxa_direita', 'coxa_esquerda', 'observacoes'
        ]
        widgets = {
            'peso': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '20',
                'max': '300',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 70.5'
            }),
            'percentual_gordura': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0',
                'max': '100',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 15.2'
            }),
            'pescoco': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '20',
                'max': '80',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'torax': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '50',
                'max': '200',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'cintura': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '40',
                'max': '200',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'quadril': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '40',
                'max': '200',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'braco_direito': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '15',
                'max': '60',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'braco_esquerdo': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '15',
                'max': '60',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'coxa_direita': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '30',
                'max': '100',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'coxa_esquerda': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '30',
                'max': '100',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Em centímetros'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre as medidas...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o auto-cálculo de IMC já que não temos altura nas medidas
        pass


class FotoProgressoForm(forms.ModelForm):
    """
    Formulário para upload de fotos de progresso.
    """
    class Meta:
        model = FotoProgresso
        fields = ['foto', 'tipo_foto', 'descricao']
        widgets = {
            'foto': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
            'tipo_foto': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Descrição da foto...'
            })
        }


class AlunoSearchForm(forms.Form):
    """
    Formulário para busca e filtro de alunos.
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por nome, email ou telefone...',
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    status = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('ativo', 'Ativos'),
            ('inativo', 'Inativos')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    objetivo = forms.ChoiceField(
        choices=[('', 'Todos')] + Aluno.OBJETIVO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
