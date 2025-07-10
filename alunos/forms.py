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
    
    dia_semana_treino = forms.ChoiceField(
        choices=[('', 'Selecione um dia')] + Aluno.DIAS_SEMANA_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    horario_treino = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    class Meta:
        model = Aluno
        fields = [
            'nome', 'email', 'telefone', 'data_nascimento',
            'sexo', 'altura', 'peso_inicial', 'objetivo',
            'observacoes', 'dia_semana_treino', 'horario_treino', 'ativo'
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
            'objetivo': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'nivel_atividade': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
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
    
    def clean(self):
        cleaned_data = super().clean()
        dia_semana = cleaned_data.get('dia_semana_treino')
        horario = cleaned_data.get('horario_treino')
        
        # Se um campo foi preenchido, o outro também deve ser
        if dia_semana and not horario:
            raise forms.ValidationError('Se você definir um dia da semana, também deve definir um horário.')
        elif horario and not dia_semana:
            raise forms.ValidationError('Se você definir um horário, também deve definir um dia da semana.')
        
        return cleaned_data


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
