"""
Formulários para gerenciamento de treinos e exercícios.
"""
from django import forms
from .models import Exercicio, PlanoTreino, TreinoDiario, ExercicioTreino
from alunos.models import Aluno


class ExercicioForm(forms.ModelForm):
    """
    Formulário para cadastro de exercícios.
    """
    class Meta:
        model = Exercicio
        fields = [
            'nome', 'descricao', 'grupo_muscular', 'categoria', 'equipamento',
            'instrucoes', 'video_url', 'imagem'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nome do exercício'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Descrição breve do exercício...'
            }),
            'grupo_muscular': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'categoria': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'equipamento': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'instrucoes': forms.Textarea(attrs={
                'rows': 5,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Instruções detalhadas de execução...'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'https://youtube.com/...'
            }),
            'imagem': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            })
        }


class PlanoTreinoForm(forms.ModelForm):
    """
    Formulário para criação de planos de treino.
    """
    class Meta:
        model = PlanoTreino
        fields = ['nome', 'descricao', 'aluno', 'duracao_semanas', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Nome do plano de treino'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Descrição e objetivos do plano...'
            }),
            'aluno': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'duracao_semanas': forms.NumberInput(attrs={
                'min': '1',
                'max': '52',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 12'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações gerais sobre o plano...'
            })
        }


class TreinoDiarioForm(forms.ModelForm):
    """
    Formulário para criação de dias de treino.
    """
    class Meta:
        model = TreinoDiario
        fields = ['dia_semana', 'nome', 'descricao', 'tempo_estimado', 'observacoes']
        widgets = {
            'dia_semana': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: Treino A - Superiores'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Descrição do treino...'
            }),
            'tempo_estimado': forms.NumberInput(attrs={
                'min': '15',
                'max': '180',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Minutos'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações específicas para este dia...'
            })
        }


class ExercicioTreinoForm(forms.ModelForm):
    """
    Formulário para adicionar exercícios aos treinos.
    """
    class Meta:
        model = ExercicioTreino
        fields = [
            'exercicio', 'series', 'repeticoes', 'carga', 
            'tempo_descanso', 'observacoes', 'ordem'
        ]
        widgets = {
            'exercicio': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'series': forms.NumberInput(attrs={
                'min': '1',
                'max': '20',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 3'
            }),
            'repeticoes': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 12-15 ou 30 seg'
            }),
            'carga': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 20kg ou Peso corporal'
            }),
            'tempo_descanso': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: 60 seg ou 1-2 min'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 2,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações específicas para este exercício...'
            }),
            'ordem': forms.NumberInput(attrs={
                'min': '1',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ordem de execução'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar exercícios por grupo muscular e nome
        self.fields['exercicio'].queryset = Exercicio.objects.all().order_by('grupo_muscular', 'nome')


class ExercicioSearchForm(forms.Form):
    """
    Formulário para busca e filtro de exercícios.
    """
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar exercícios...',
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    grupo_muscular = forms.ChoiceField(
        choices=[('', 'Todos os grupos')] + Exercicio.GRUPO_MUSCULAR_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    equipamento = forms.ChoiceField(
        choices=[('', 'Todos os equipamentos')] + Exercicio.EQUIPAMENTO_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
