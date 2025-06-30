"""
Views para controle de frequência dos alunos.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

from .models import RegistroPresenca, AgendaAula, RelatorioFrequencia
from .forms import RegistroPresencaForm, AgendaAulaForm, FiltroFrequenciaForm, AgendaStatusForm
from alunos.models import Aluno


class FrequenciaListView(LoginRequiredMixin, ListView):
    """
    Lista os registros de frequência com filtros.
    """
    model = RegistroPresenca
    template_name = 'frequencia/lista.html'
    context_object_name = 'registros'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = RegistroPresenca.objects.filter(
            aluno__personal_trainer=self.request.user
        ).select_related('aluno')
        
        # Aplicar filtros
        form = FiltroFrequenciaForm(self.request.user, self.request.GET)
        if form.is_valid():
            if form.cleaned_data['aluno']:
                queryset = queryset.filter(aluno=form.cleaned_data['aluno'])
            if form.cleaned_data['mes']:
                queryset = queryset.filter(data_aula__month=form.cleaned_data['mes'])
            if form.cleaned_data['ano']:
                queryset = queryset.filter(data_aula__year=form.cleaned_data['ano'])
            if form.cleaned_data['status']:
                queryset = queryset.filter(status=form.cleaned_data['status'])
        
        return queryset.order_by('-data_aula', 'horario_inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtro_form'] = FiltroFrequenciaForm(self.request.user, self.request.GET)
        
        # Estatísticas gerais
        total_registros = self.get_queryset().count()
        presencas = self.get_queryset().filter(status='presente').count()
        faltas = self.get_queryset().filter(status='falta').count()
        
        context['stats'] = {
            'total_registros': total_registros,
            'presencas': presencas,
            'faltas': faltas,
            'percentual_presenca': round((presencas / total_registros * 100) if total_registros > 0 else 0, 1)
        }
        
        return context


class RegistroPresencaCreateView(LoginRequiredMixin, CreateView):
    """
    Criar novo registro de presença.
    """
    model = RegistroPresenca
    form_class = RegistroPresencaForm
    template_name = 'frequencia/registrar_presenca.html'
    success_url = reverse_lazy('frequencia:lista')
    
    def form_valid(self, form):
        messages.success(self.request, 'Presença registrada com sucesso!')
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas alunos do personal trainer logado
        form.fields['aluno'].queryset = Aluno.objects.filter(
            personal_trainer=self.request.user,
            ativo=True
        )
        return form


class AgendaListView(LoginRequiredMixin, ListView):
    """
    Lista os agendamentos de aulas.
    """
    model = AgendaAula
    template_name = 'frequencia/agenda.html'
    context_object_name = 'agendamentos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = AgendaAula.objects.filter(
            aluno__personal_trainer=self.request.user
        ).select_related('aluno')
        
        # Filtrar por data se fornecida
        data_filtro = self.request.GET.get('data')
        if data_filtro:
            try:
                data = datetime.strptime(data_filtro, '%Y-%m-%d').date()
                queryset = queryset.filter(data_aula=data)
            except ValueError:
                pass
        
        # Filtrar por status
        status_filtro = self.request.GET.get('status')
        if status_filtro:
            queryset = queryset.filter(status=status_filtro)
        
        return queryset.order_by('data_aula', 'horario_inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Próximas aulas (próximos 7 dias)
        hoje = timezone.now().date()
        proximas_aulas = AgendaAula.objects.filter(
            aluno__personal_trainer=self.request.user,
            data_aula__gte=hoje,
            data_aula__lte=hoje + timedelta(days=7),
            status__in=['agendado', 'confirmado']
        ).order_by('data_aula', 'horario_inicio')
        
        context['proximas_aulas'] = proximas_aulas
        context['data_filtro'] = self.request.GET.get('data', '')
        context['status_filtro'] = self.request.GET.get('status', '')
        context['status_choices'] = AgendaAula.STATUS_CHOICES
        
        return context


class AgendaCreateView(LoginRequiredMixin, CreateView):
    """
    Agendar nova aula.
    """
    model = AgendaAula
    form_class = AgendaAulaForm
    template_name = 'frequencia/agendar_aula.html'
    success_url = reverse_lazy('frequencia:agenda')
    
    def form_valid(self, form):
        messages.success(self.request, 'Aula agendada com sucesso!')
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas alunos do personal trainer logado
        form.fields['aluno'].queryset = Aluno.objects.filter(
            personal_trainer=self.request.user,
            ativo=True
        )
        return form


@login_required
def alterar_status_agenda(request, agenda_id):
    """
    Alterar status de um agendamento.
    """
    agenda = get_object_or_404(
        AgendaAula, 
        id=agenda_id, 
        aluno__personal_trainer=request.user
    )
    
    if request.method == 'POST':
        form = AgendaStatusForm(request.POST)
        if form.is_valid():
            agenda.status = form.cleaned_data['status']
            if form.cleaned_data['observacoes']:
                agenda.observacoes = form.cleaned_data['observacoes']
            agenda.save()
            
            messages.success(request, f'Status alterado para "{agenda.get_status_display()}"')
            return redirect('frequencia:agenda')
    else:
        form = AgendaStatusForm(initial={'status': agenda.status})
    
    return render(request, 'frequencia/alterar_status.html', {
        'form': form,
        'agenda': agenda
    })


@login_required
def calendario_mensal(request):
    """
    Visualização de calendário mensal com agendamentos.
    """
    hoje = timezone.now().date()
    mes = int(request.GET.get('mes', hoje.month))
    ano = int(request.GET.get('ano', hoje.year))
    
    # Criar calendário
    cal = calendar.Calendar(firstweekday=6)  # Domingo como primeiro dia
    dias_mes = cal.monthdayscalendar(ano, mes)
    
    # Buscar agendamentos do mês
    agendamentos = AgendaAula.objects.filter(
        aluno__personal_trainer=request.user,
        data_aula__month=mes,
        data_aula__year=ano
    ).select_related('aluno').order_by('data_aula', 'horario_inicio')
    
    # Organizar agendamentos por dia
    agendamentos_por_dia = {}
    for agenda in agendamentos:
        dia = agenda.data_aula.day
        if dia not in agendamentos_por_dia:
            agendamentos_por_dia[dia] = []
        agendamentos_por_dia[dia].append(agenda)
    
    # Navegação
    mes_anterior = mes - 1 if mes > 1 else 12
    ano_anterior = ano if mes > 1 else ano - 1
    mes_proximo = mes + 1 if mes < 12 else 1
    ano_proximo = ano if mes < 12 else ano + 1
    
    context = {
        'dias_mes': dias_mes,
        'agendamentos_por_dia': agendamentos_por_dia,
        'mes_atual': mes,
        'ano_atual': ano,
        'nome_mes': calendar.month_name[mes],
        'mes_anterior': mes_anterior,
        'ano_anterior': ano_anterior,
        'mes_proximo': mes_proximo,
        'ano_proximo': ano_proximo,
        'hoje': hoje,
    }
    
    return render(request, 'frequencia/calendario.html', context)


@login_required
def relatorio_frequencia_aluno(request, aluno_id):
    """
    Relatório detalhado de frequência de um aluno.
    """
    aluno = get_object_or_404(
        Aluno, 
        id=aluno_id, 
        personal_trainer=request.user
    )
    
    # Período do relatório
    mes = int(request.GET.get('mes', timezone.now().month))
    ano = int(request.GET.get('ano', timezone.now().year))
    
    # Buscar ou gerar relatório
    relatorio = RelatorioFrequencia.gerar_relatorio_mensal(aluno, mes, ano)
    
    # Registros do período
    registros = RegistroPresenca.objects.filter(
        aluno=aluno,
        data_aula__month=mes,
        data_aula__year=ano
    ).order_by('data_aula')
    
    # Estatísticas por semana
    semanas = {}
    for registro in registros:
        semana = registro.data_aula.isocalendar()[1]
        if semana not in semanas:
            semanas[semana] = {
                'presencas': 0,
                'faltas': 0,
                'total': 0
            }
        semanas[semana]['total'] += 1
        if registro.status == 'presente':
            semanas[semana]['presencas'] += 1
        else:
            semanas[semana]['faltas'] += 1
    
    context = {
        'aluno': aluno,
        'relatorio': relatorio,
        'registros': registros,
        'semanas': semanas,
        'mes': mes,
        'ano': ano,
        'nome_mes': calendar.month_name[mes],
    }
    
    return render(request, 'frequencia/relatorio_aluno.html', context)


@login_required
def dashboard_frequencia(request):
    """
    Dashboard com estatísticas de frequência.
    """
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # Aulas de hoje
    aulas_hoje = AgendaAula.objects.filter(
        aluno__personal_trainer=request.user,
        data_aula=hoje
    ).select_related('aluno')
    
    # Estatísticas do mês atual
    registros_mes = RegistroPresenca.objects.filter(
        aluno__personal_trainer=request.user,
        data_aula__month=mes_atual,
        data_aula__year=ano_atual
    )
    
    # Top alunos por frequência
    alunos_stats = []
    for aluno in Aluno.objects.filter(personal_trainer=request.user, ativo=True):
        registros_aluno = registros_mes.filter(aluno=aluno)
        total = registros_aluno.count()
        presencas = registros_aluno.filter(status='presente').count()
        
        if total > 0:
            percentual = round((presencas / total) * 100, 1)
            alunos_stats.append({
                'aluno': aluno,
                'total_aulas': total,
                'presencas': presencas,
                'percentual': percentual
            })
    
    # Ordenar por percentual de frequência
    alunos_stats.sort(key=lambda x: x['percentual'], reverse=True)
    
    context = {
        'aulas_hoje': aulas_hoje,
        'total_registros_mes': registros_mes.count(),
        'presencas_mes': registros_mes.filter(status='presente').count(),
        'faltas_mes': registros_mes.filter(status='falta').count(),
        'alunos_stats': alunos_stats[:10],  # Top 10
    }
    
    return render(request, 'frequencia/dashboard.html', context)
