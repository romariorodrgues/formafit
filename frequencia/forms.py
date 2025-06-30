"""
Formulários para controle de frequência.
"""
from django import forms
from .models import RegistroPresenca, AgendaAula
from alunos.models import Aluno


class RegistroPresencaForm(forms.ModelForm):
    """
    Formulário para registro de presença.
    """
    class Meta:
        model = RegistroPresenca
        fields = ['aluno', 'data_aula', 'horario_inicio', 'horario_fim', 'status', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'data_aula': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'horario_inicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'horario_fim': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre a aula...'
            })
        }


class AgendaAulaForm(forms.ModelForm):
    """
    Formulário para agendamento de aulas.
    """
    class Meta:
        model = AgendaAula
        fields = ['aluno', 'data_aula', 'horario_inicio', 'horario_fim', 'tipo_treino', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'data_aula': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'horario_inicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'horario_fim': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            }),
            'tipo_treino': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Ex: Treino A, Avaliação, Cardio'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                'placeholder': 'Observações sobre a aula...'
            })
        }


class FiltroFrequenciaForm(forms.Form):
    """
    Formulário para filtrar registros de frequência.
    """
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.all(),
        required=False,
        empty_label="Todos os alunos",
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    mes = forms.ChoiceField(
        choices=[('', 'Todos os meses')] + [(i, f"{i:02d}") for i in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    ano = forms.ChoiceField(
        choices=[('', 'Todos os anos')] + [(i, str(i)) for i in range(2020, 2030)],
        required=False,
        widget=forms.Select(attrs={
            'class': 'block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'Todos os status')] + RegistroPresenca.STATUS_CHOICES,
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


class AgendaStatusForm(forms.Form):
    """
    Formulário para alterar status de agendamento.
    """
    STATUS_CHOICES = AgendaAula.STATUS_CHOICES
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    
    observacoes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Observações sobre a alteração...'
        })
    )
