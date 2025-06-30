"""
Views para autenticação e dashboard.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import User
from .forms import UserRegistrationForm, UserUpdateForm
from alunos.models import Aluno
from financeiro.models import Fatura
from frequencia.models import AgendaAula
from notificacoes.models import Notificacao


class CustomLoginView(LoginView):
    """
    View customizada para login com template moderno.
    """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')


class RegisterView(CreateView):
    """
    View para registro de novos personal trainers.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Cadastro realizado com sucesso! Bem-vindo ao FormaFit!')
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard principal do personal trainer.
    """
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        hoje = timezone.now().date()
        
        # Estatísticas básicas
        context['total_alunos'] = Aluno.objects.filter(personal_trainer=user, ativo=True).count()
        context['total_alunos_inativos'] = Aluno.objects.filter(personal_trainer=user, ativo=False).count()
        
        # Aulas de hoje
        context['aulas_hoje'] = AgendaAula.objects.filter(
            aluno__personal_trainer=user,
            data_aula=hoje,
            status__in=['agendado', 'confirmado']
        ).order_by('horario_inicio')
        
        # Próximas aulas (próximos 3 dias)
        proximos_dias = hoje + timedelta(days=3)
        context['proximas_aulas'] = AgendaAula.objects.filter(
            aluno__personal_trainer=user,
            data_aula__range=[hoje + timedelta(days=1), proximos_dias],
            status__in=['agendado', 'confirmado']
        ).order_by('data_aula', 'horario_inicio')[:5]
        
        # Faturas vencidas
        context['faturas_vencidas'] = Fatura.objects.filter(
            aluno__personal_trainer=user,
            status__in=['pendente', 'parcial'],
            data_vencimento__lt=hoje
        ).count()
        
        # Faturas que vencem hoje
        context['faturas_vencem_hoje'] = Fatura.objects.filter(
            aluno__personal_trainer=user,
            status__in=['pendente', 'parcial'],
            data_vencimento=hoje
        ).count()
        
        # Notificações não lidas
        context['notificacoes_nao_lidas'] = Notificacao.objects.filter(
            personal_trainer=user,
            status='enviada'
        ).count()
        
        # Últimas notificações
        context['ultimas_notificacoes'] = Notificacao.objects.filter(
            personal_trainer=user
        ).order_by('-data_criacao')[:5]
        
        # Receita do mês atual
        mes_atual = hoje.month
        ano_atual = hoje.year
        faturas_mes = Fatura.objects.filter(
            aluno__personal_trainer=user,
            mes_referencia=mes_atual,
            ano_referencia=ano_atual
        )
        context['receita_prevista_mes'] = sum(f.valor_final for f in faturas_mes)
        context['receita_recebida_mes'] = sum(f.valor_final for f in faturas_mes if f.status == 'paga')
        
        # Alunos mais ativos (por frequência)
        context['alunos_ativos'] = Aluno.objects.filter(
            personal_trainer=user,
            ativo=True
        ).annotate(
            treinos_mes=Count(
                'registros_treino',
                filter=Q(registros_treino__data_execucao__month=mes_atual)
            )
        ).order_by('-treinos_mes')[:5]
        
        return context


class PerfilView(LoginRequiredMixin, UpdateView):
    """
    View para edição do perfil do personal trainer.
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/perfil.html'
    success_url = reverse_lazy('accounts:perfil')
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Estatísticas para o perfil
        context['total_alunos'] = Aluno.objects.filter(personal_trainer=user, ativo=True).count()
        
        # Importar modelos necessários para as estatísticas
        try:
            from treinos.models import PlanoTreino
            context['total_treinos'] = PlanoTreino.objects.filter(personal_trainer=user).count()
        except ImportError:
            context['total_treinos'] = 0
        
        try:
            from frequencia.models import RegistroPresenca
            context['total_aulas'] = RegistroPresenca.objects.filter(
                aluno__personal_trainer=user,
                status='presente'
            ).count()
        except (ImportError, Exception):
            context['total_aulas'] = 0
            
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)


class ConfiguracoesView(LoginRequiredMixin, TemplateView):
    """
    View para configurações gerais do sistema.
    """
    template_name = 'accounts/configuracoes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar configurações específicas aqui
        return context


class PerfilTestView(LoginRequiredMixin, TemplateView):
    """
    View de teste para o perfil.
    """
    template_name = 'accounts/perfil_test.html'


class TesteRolagemView(LoginRequiredMixin, TemplateView):
    """
    View de teste para verificar rolagem.
    """
    template_name = 'teste_rolagem.html'
