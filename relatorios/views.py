"""
Views para geração e gerenciamento de relatórios.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, FormView
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, FileResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q, Avg, Count
from datetime import datetime, timedelta
import json
import os

from .models import RelatorioProgresso, TipoRelatorio
from .forms import GerarRelatorioForm, FiltroRelatoriosForm
from .services import RelatorioService
from alunos.models import Aluno, MedidasCorporais
from frequencia.models import RegistroPresenca


@login_required
def lista_relatorios(request):
    """Lista de relatórios gerados."""
    # Filtros
    filtro_form = FiltroRelatoriosForm(request.GET, user=request.user)
    
    # Queryset base
    relatorios = RelatorioProgresso.objects.filter(
        personal_trainer=request.user
    ).select_related('aluno', 'tipo_relatorio').order_by('-data_geracao')
    
    # Aplicar filtros
    if filtro_form.is_valid():
        if filtro_form.cleaned_data['aluno']:
            relatorios = relatorios.filter(aluno=filtro_form.cleaned_data['aluno'])
        
        if filtro_form.cleaned_data['periodo']:
            relatorios = relatorios.filter(periodo=filtro_form.cleaned_data['periodo'])
        
        if filtro_form.cleaned_data['status']:
            relatorios = relatorios.filter(status=filtro_form.cleaned_data['status'])
        
        if filtro_form.cleaned_data['data_inicio']:
            relatorios = relatorios.filter(data_inicio__gte=filtro_form.cleaned_data['data_inicio'])
        
        if filtro_form.cleaned_data['data_fim']:
            relatorios = relatorios.filter(data_fim__lte=filtro_form.cleaned_data['data_fim'])
    
    # Estatísticas
    total_relatorios = relatorios.count()
    relatorios_concluidos = relatorios.filter(status='concluido').count()
    relatorios_erro = relatorios.filter(status='erro').count()
    
    context = {
        'relatorios': relatorios,
        'filtro_form': filtro_form,
        'total_relatorios': total_relatorios,
        'relatorios_concluidos': relatorios_concluidos,
        'relatorios_erro': relatorios_erro,
    }
    
    return render(request, 'relatorios/lista.html', context)


class RelatorioListView(LoginRequiredMixin, ListView):
    """Lista de relatórios gerados."""
    model = RelatorioProgresso
    template_name = 'relatorios/lista.html'
    context_object_name = 'relatorios'
    paginate_by = 20
    
    def get_queryset(self):
        return RelatorioProgresso.objects.filter(
            personal_trainer=self.request.user
        ).select_related('aluno', 'tipo_relatorio').order_by('-data_geracao')


@login_required
def gerar_relatorio_view(request):
    """View para gerar novo relatório."""
    if request.method == 'POST':
        form = GerarRelatorioForm(request.POST, user=request.user)
        if form.is_valid():
            relatorio = form.save(commit=False)
            relatorio.personal_trainer = request.user
            relatorio.save()
            
            # Gerar relatório em background (ou de forma síncrona para demonstração)
            try:
                service = RelatorioService()
                relatorio_gerado = service.gerar_relatorio_progresso(relatorio.id)
                messages.success(request, f'Relatório "{relatorio_gerado.titulo}" gerado com sucesso!')
                return redirect('relatorios:detalhe', pk=relatorio.id)
            except Exception as e:
                messages.error(request, f'Erro ao gerar relatório: {str(e)}')
                return redirect('relatorios:lista')
    else:
        form = GerarRelatorioForm(user=request.user)
    
    return render(request, 'relatorios/gerar.html', {'form': form})


@login_required
def relatorio_detail_view(request, pk):
    """View para visualizar detalhes do relatório."""
    relatorio = get_object_or_404(
        RelatorioProgresso,
        pk=pk,
        personal_trainer=request.user
    )
    
    context = {
        'relatorio': relatorio,
        'pode_regenerar': relatorio.status in ['erro', 'concluido'],
    }
    
    return render(request, 'relatorios/detalhe.html', context)


@login_required
def download_relatorio_view(request, pk):
    """View para download do relatório em PDF."""
    relatorio = get_object_or_404(
        RelatorioProgresso,
        pk=pk,
        personal_trainer=request.user
    )
    
    if not relatorio.arquivo_pdf or relatorio.status != 'concluido':
        messages.error(request, 'Relatório não está disponível para download.')
        return redirect('relatorios:detalhe', pk=pk)
    
    try:
        return FileResponse(
            open(relatorio.arquivo_pdf.path, 'rb'),
            as_attachment=True,
            filename=f"relatorio_{relatorio.aluno.nome}_{relatorio.data_inicio}.pdf"
        )
    except FileNotFoundError:
        messages.error(request, 'Arquivo do relatório não encontrado.')
        return redirect('relatorios:detalhe', pk=pk)


@login_required
def regenerar_relatorio_view(request, pk):
    """View para regenerar um relatório."""
    relatorio = get_object_or_404(
        RelatorioProgresso,
        pk=pk,
        personal_trainer=request.user
    )
    
    if request.method == 'POST':
        try:
            service = RelatorioService()
            relatorio_gerado = service.gerar_relatorio_progresso(relatorio.id)
            messages.success(request, f'Relatório "{relatorio_gerado.titulo}" regenerado com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao regenerar relatório: {str(e)}')
        
        return redirect('relatorios:detalhe', pk=pk)
    
    return render(request, 'relatorios/confirmar_regenerar.html', {'relatorio': relatorio})


@login_required
def dashboard_relatorios_view(request):
    """Dashboard com estatísticas dos relatórios."""
    relatorios = RelatorioProgresso.objects.filter(personal_trainer=request.user)
    
    # Estatísticas gerais
    total_relatorios = relatorios.count()
    relatorios_mes = relatorios.filter(
        data_geracao__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Relatórios por status
    stats_status = {}
    for status, label in RelatorioProgresso.STATUS_CHOICES:
        stats_status[status] = {
            'label': label,
            'count': relatorios.filter(status=status).count()
        }
    
    # Relatórios por período
    stats_periodo = {}
    for periodo, label in RelatorioProgresso.PERIODO_CHOICES:
        stats_periodo[periodo] = {
            'label': label,
            'count': relatorios.filter(periodo=periodo).count()
        }
    
    # Alunos com mais relatórios
    from django.db.models import Count
    alunos_top = relatorios.values('aluno__nome').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    # Últimos relatórios
    ultimos_relatorios = relatorios.select_related('aluno').order_by('-data_geracao')[:10]
    
    context = {
        'total_relatorios': total_relatorios,
        'relatorios_mes': relatorios_mes,
        'stats_status': stats_status,
        'stats_periodo': stats_periodo,
        'alunos_top': alunos_top,
        'ultimos_relatorios': ultimos_relatorios,
    }
    
    return render(request, 'relatorios/dashboard.html', context)


@login_required
def enviar_relatorio_email_view(request, pk):
    """View para enviar relatório por email."""
    relatorio = get_object_or_404(
        RelatorioProgresso,
        pk=pk,
        personal_trainer=request.user
    )
    
    if request.method == 'POST':
        # TODO: Implementar envio por email
        messages.info(request, 'Funcionalidade de envio por email será implementada em breve.')
        return redirect('relatorios:detalhe', pk=pk)
    
    return render(request, 'relatorios/enviar_email.html', {'relatorio': relatorio})


@login_required
def ajax_status_relatorio(request, pk):
    """Retorna o status atual de um relatório via AJAX."""
    try:
        relatorio = RelatorioProgresso.objects.get(
            pk=pk,
            personal_trainer=request.user
        )
        return JsonResponse({
            'status': relatorio.status,
            'progresso': relatorio.get_status_display(),
            'url_download': relatorio.url_download,
        })
    except RelatorioProgresso.DoesNotExist:
        return JsonResponse({'error': 'Relatório não encontrado'}, status=404)


class GerarRelatorioView(LoginRequiredMixin, FormView):
    """View baseada em classe para gerar relatório."""
    template_name = 'relatorios/gerar.html'
    form_class = GerarRelatorioForm
    success_url = reverse_lazy('relatorios:lista')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        relatorio = form.save(commit=False)
        relatorio.personal_trainer = self.request.user
        relatorio.save()
        
        try:
            service = RelatorioService()
            relatorio_gerado = service.gerar_relatorio_progresso(relatorio.id)
            messages.success(self.request, f'Relatório "{relatorio_gerado.titulo}" gerado com sucesso!')
        except Exception as e:
            messages.error(self.request, f'Erro ao gerar relatório: {str(e)}')
        
        return super().form_valid(form)


class GerarRelatoriosMultiplosView(LoginRequiredMixin, FormView):
    """Gerar múltiplos relatórios para vários alunos."""
    template_name = 'relatorios/gerar_multiplos.html'
    
    def get(self, request, *args, **kwargs):
        # TODO: Implementar geração de múltiplos relatórios
        messages.info(request, 'Funcionalidade de múltiplos relatórios será implementada em breve.')
        return redirect('relatorios:lista')


class RelatorioDetailView(LoginRequiredMixin, DetailView):
    """Detalhes do relatório."""
    model = RelatorioProgresso
    template_name = 'relatorios/detalhe.html'
    context_object_name = 'relatorio'
    
    def get_queryset(self):
        return RelatorioProgresso.objects.filter(personal_trainer=self.request.user)


class DownloadRelatorioView(LoginRequiredMixin, DetailView):
    """Download de relatório."""
    model = RelatorioProgresso
    
    def get_queryset(self):
        return RelatorioProgresso.objects.filter(personal_trainer=self.request.user)
    
    def get(self, request, *args, **kwargs):
        relatorio = self.get_object()
        
        if not relatorio.arquivo_pdf or relatorio.status != 'concluido':
            messages.error(request, 'Relatório não está disponível para download.')
            return redirect('relatorios:detalhe', pk=relatorio.pk)
        
        try:
            return FileResponse(
                open(relatorio.arquivo_pdf.path, 'rb'),
                as_attachment=True,
                filename=f"relatorio_{relatorio.aluno.nome}_{relatorio.data_inicio}.pdf"
            )
        except FileNotFoundError:
            messages.error(request, 'Arquivo do relatório não encontrado.')
            return redirect('relatorios:detalhe', pk=relatorio.pk)


class EnviarRelatorioEmailView(LoginRequiredMixin, DetailView):
    """Enviar relatório por email."""
    
    def get(self, request, *args, **kwargs):
        # TODO: Implementar envio por email
        messages.info(request, 'Funcionalidade de envio por email será implementada em breve.')
        return redirect('relatorios:lista')
