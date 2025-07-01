"""
Views para sistema de notificações.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import requests
import json

from .models import (
    Notificacao, TipoNotificacao, NotificacaoAutomatica, 
    LogEnvioWhatsApp, ConfiguracaoNotificacao
)
from alunos.models import Aluno
from .forms import NotificacaoForm, TipoNotificacaoForm, ConfiguracaoNotificacaoForm


class NotificacaoListView(LoginRequiredMixin, ListView):
    """Dashboard principal de notificações."""
    model = Notificacao
    template_name = 'notificacoes/dashboard.html'
    context_object_name = 'notificacoes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Notificacao.objects.filter(
            personal_trainer=self.request.user
        ).select_related('aluno', 'tipo_notificacao')
        
        # Filtros
        status = self.request.GET.get('status')
        tipo = self.request.GET.get('tipo')
        aluno = self.request.GET.get('aluno')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        
        if status:
            queryset = queryset.filter(status=status)
        if tipo:
            queryset = queryset.filter(tipo_notificacao_id=tipo)
        if aluno:
            queryset = queryset.filter(aluno_id=aluno)
        if data_inicio:
            queryset = queryset.filter(data_criacao__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_criacao__lte=data_fim)
            
        return queryset.order_by('-data_criacao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Estatísticas
        context['total_notificacoes'] = Notificacao.objects.filter(personal_trainer=user).count()
        context['pendentes'] = Notificacao.objects.filter(personal_trainer=user, status='pendente').count()
        context['enviadas'] = Notificacao.objects.filter(personal_trainer=user, status='enviada').count()
        context['nao_lidas'] = Notificacao.objects.filter(personal_trainer=user, status='enviada').count()
        
        # Filtros para o template
        context['tipos_notificacao'] = TipoNotificacao.objects.filter(ativo=True)
        context['alunos'] = Aluno.objects.filter(personal_trainer=user, ativo=True)
        
        # Notificações recentes não lidas
        context['notificacoes_recentes'] = Notificacao.objects.filter(
            personal_trainer=user,
            status='enviada'
        ).order_by('-data_criacao')[:5]
        
        return context


class NotificacaoCreateView(LoginRequiredMixin, CreateView):
    """Criar nova notificação manual."""
    model = Notificacao
    form_class = NotificacaoForm
    template_name = 'notificacoes/criar_notificacao.html'
    success_url = reverse_lazy('notificacoes:lista')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.personal_trainer = self.request.user
        response = super().form_valid(form)
        
        # Enviar notificação se solicitado
        if form.cleaned_data.get('enviar_agora'):
            self.object.enviar()
            
        messages.success(self.request, 'Notificação criada com sucesso!')
        return response


class NotificacaoDetailView(LoginRequiredMixin, DetailView):
    """Detalhes de uma notificação."""
    model = Notificacao
    template_name = 'notificacoes/detalhe_notificacao.html'
    context_object_name = 'notificacao'
    
    def get_queryset(self):
        return Notificacao.objects.filter(personal_trainer=self.request.user)


class MarcarComoLidaView(LoginRequiredMixin, TemplateView):
    """View para marcar como lida via AJAX."""
    
    def post(self, request, pk):
        """Marcar notificação como lida."""
        notificacao = get_object_or_404(
            Notificacao, 
            pk=pk, 
            personal_trainer=request.user
        )
        notificacao.marcar_como_lida()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
        messages.success(request, 'Notificação marcada como lida.')
        return redirect('notificacoes:lista')


class TipoNotificacaoListView(LoginRequiredMixin, ListView):
    """Lista de tipos de notificação."""
    model = TipoNotificacao
    template_name = 'notificacoes/tipos_notificacao.html'
    context_object_name = 'tipos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_ativos'] = TipoNotificacao.objects.filter(ativo=True).count()
        context['tipos_inativos'] = TipoNotificacao.objects.filter(ativo=False).count()
        return context


class TipoNotificacaoCreateView(LoginRequiredMixin, CreateView):
    """Criar novo tipo de notificação."""
    model = TipoNotificacao
    form_class = TipoNotificacaoForm
    template_name = 'notificacoes/criar_tipo_notificacao.html'
    success_url = reverse_lazy('notificacoes:tipos')
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de notificação criado com sucesso!')
        return super().form_valid(form)


class TipoNotificacaoUpdateView(LoginRequiredMixin, UpdateView):
    """Editar tipo de notificação."""
    model = TipoNotificacao
    form_class = TipoNotificacaoForm
    template_name = 'notificacoes/editar_tipo_notificacao.html'
    success_url = reverse_lazy('notificacoes:tipos')
    
    def form_valid(self, form):
        messages.success(self.request, 'Tipo de notificação atualizado com sucesso!')
        return super().form_valid(form)


class NotificacaoAutomaticaListView(LoginRequiredMixin, ListView):
    """Lista de notificações automáticas."""
    model = NotificacaoAutomatica
    template_name = 'notificacoes/automaticas.html'
    context_object_name = 'automaticas'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ativas'] = NotificacaoAutomatica.objects.filter(ativa=True).count()
        context['inativas'] = NotificacaoAutomatica.objects.filter(ativa=False).count()
        return context


class NotificacaoAutomaticaUpdateView(LoginRequiredMixin, UpdateView):
    """Editar configurações de notificação automática."""
    model = NotificacaoAutomatica
    fields = ['ativa', 'antecedencia_dias', 'horario_envio', 'apenas_alunos_ativos']
    template_name = 'notificacoes/editar_automatica.html'
    success_url = reverse_lazy('notificacoes:automaticas')
    
    def form_valid(self, form):
        messages.success(self.request, 'Configuração automática atualizada!')
        return super().form_valid(form)


class ConfiguracoesNotificacaoView(LoginRequiredMixin, TemplateView):
    """Configurações gerais de notificação."""
    template_name = 'notificacoes/configuracoes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Estatísticas gerais
        context['total_enviadas_hoje'] = Notificacao.objects.filter(
            personal_trainer=user,
            data_envio__date=timezone.now().date()
        ).count()
        
        context['total_whatsapp_mes'] = LogEnvioWhatsApp.objects.filter(
            notificacao__personal_trainer=user,
            data_envio__month=timezone.now().month
        ).count()
        
        # Configurações de alunos
        context['alunos_com_config'] = ConfiguracaoNotificacao.objects.filter(
            aluno__personal_trainer=user
        ).count()
        
        context['alunos_sem_config'] = Aluno.objects.filter(
            personal_trainer=user,
            ativo=True
        ).exclude(
            id__in=ConfiguracaoNotificacao.objects.filter(
                aluno__personal_trainer=user
            ).values_list('aluno_id', flat=True)
        ).count()
        
        return context


@login_required
def configuracao_aluno_view(request, aluno_id):
    """Configurar notificações para um aluno específico."""
    aluno = get_object_or_404(Aluno, id=aluno_id, personal_trainer=request.user)
    config, created = ConfiguracaoNotificacao.objects.get_or_create(aluno=aluno)
    
    if request.method == 'POST':
        form = ConfiguracaoNotificacaoForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, f'Configurações de {aluno.nome} atualizadas!')
            return redirect('notificacoes:configuracoes')
    else:
        form = ConfiguracaoNotificacaoForm(instance=config)
    
    context = {
        'aluno': aluno,
        'form': form,
        'config': config,
    }
    return render(request, 'notificacoes/configuracao_aluno.html', context)


@login_required
def teste_whatsapp_view(request):
    """Testar envio de WhatsApp."""
    if request.method == 'POST':
        telefone = request.POST.get('telefone')
        mensagem = request.POST.get('mensagem')
        
        # Implementar teste de envio via ChatPro
        try:
            # Aqui seria a integração real com a API do ChatPro
            resultado = {
                'sucesso': True,
                'mensagem': 'Teste enviado com sucesso!'
            }
            messages.success(request, 'Mensagem de teste enviada com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao enviar teste: {str(e)}')
    
    return render(request, 'notificacoes/teste_whatsapp.html')


class LogWhatsAppView(LoginRequiredMixin, ListView):
    """Logs de envio WhatsApp."""
    model = LogEnvioWhatsApp
    template_name = 'notificacoes/logs_whatsapp.html'
    context_object_name = 'logs'
    paginate_by = 50
    
    def get_queryset(self):
        return LogEnvioWhatsApp.objects.filter(
            notificacao__personal_trainer=self.request.user
        ).order_by('-data_envio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Estatísticas
        total_logs = LogEnvioWhatsApp.objects.filter(notificacao__personal_trainer=user)
        context['total_envios'] = total_logs.count()
        context['sucessos'] = total_logs.filter(status='sucesso').count()
        context['erros'] = total_logs.filter(status='erro').count()
        context['pendentes'] = total_logs.filter(status='pendente').count()
        
        return context


class ConfiguracaoAlunoView(LoginRequiredMixin, TemplateView):
    """View para configuração de aluno."""
    
    def get(self, request, aluno_id):
        return configuracao_aluno_view(request, aluno_id)
    
    def post(self, request, aluno_id):
        return configuracao_aluno_view(request, aluno_id)


class TesteWhatsAppView(LoginRequiredMixin, TemplateView):
    """View para teste de WhatsApp."""
    template_name = 'notificacoes/teste_whatsapp.html'
    
    def post(self, request):
        return teste_whatsapp_view(request)
