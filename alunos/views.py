"""
Views para gerenciamento de alunos.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse

from .models import Aluno, MedidasCorporais, FotoProgresso
from .forms import AlunoForm, MedidasCorporaisForm, FotoProgressoForm


class AlunosListView(LoginRequiredMixin, ListView):
    """
    Lista todos os alunos do personal trainer.
    """
    model = Aluno
    template_name = 'alunos/lista.html'
    context_object_name = 'alunos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Aluno.objects.filter(personal_trainer=self.request.user)
        
        # Filtros
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        objetivo = self.request.GET.get('objetivo')
        
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(email__icontains=search) |
                Q(telefone__icontains=search)
            )
        
        if status == 'ativo':
            queryset = queryset.filter(ativo=True)
        elif status == 'inativo':
            queryset = queryset.filter(ativo=False)
        
        if objetivo:
            queryset = queryset.filter(objetivo__icontains=objetivo)
        
        return queryset.order_by('-data_criacao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['objetivo'] = self.request.GET.get('objetivo', '')
        
        # Estatísticas
        context['total_alunos'] = Aluno.objects.filter(personal_trainer=self.request.user).count()
        context['alunos_ativos'] = Aluno.objects.filter(personal_trainer=self.request.user, ativo=True).count()
        context['alunos_inativos'] = Aluno.objects.filter(personal_trainer=self.request.user, ativo=False).count()
        
        return context


class AlunoCreateView(LoginRequiredMixin, CreateView):
    """
    Cadastro de novo aluno.
    """
    model = Aluno
    form_class = AlunoForm
    template_name = 'alunos/cadastrar.html'
    success_url = reverse_lazy('alunos:lista')
    
    def form_valid(self, form):
        form.instance.personal_trainer = self.request.user
        messages.success(self.request, f'Aluno {form.instance.nome} cadastrado com sucesso!')
        return super().form_valid(form)


class AlunoUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edição de dados do aluno.
    """
    model = Aluno
    form_class = AlunoForm
    template_name = 'alunos/editar.html'
    
    def get_queryset(self):
        return Aluno.objects.filter(personal_trainer=self.request.user)
    
    def get_success_url(self):
        return reverse('alunos:detalhes', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f'Dados de {form.instance.nome} atualizados com sucesso!')
        return super().form_valid(form)


class AlunoDetailView(LoginRequiredMixin, DetailView):
    """
    Detalhes completos do aluno com histórico de medidas e treinos.
    """
    model = Aluno
    template_name = 'alunos/detalhes.html'
    context_object_name = 'aluno'
    
    def get_queryset(self):
        return Aluno.objects.filter(personal_trainer=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aluno = self.object
        
        # Medidas corporais (últimas 10)
        context['medidas'] = MedidasCorporais.objects.filter(aluno=aluno).order_by('-data_medicao')[:10]
        context['ultima_medida'] = context['medidas'].first() if context['medidas'] else None
        
        # Fotos de progresso (últimas 6)
        context['fotos'] = FotoProgresso.objects.filter(aluno=aluno).order_by('-data_foto')[:6]
        
        # Estatísticas de frequência (último mês)
        mes_passado = timezone.now() - timedelta(days=30)
        from frequencia.models import RegistroPresenca
        context['presencas_mes'] = RegistroPresenca.objects.filter(
            aluno=aluno,
            data_presenca__gte=mes_passado,
            presente=True
        ).count()
        
        # Plano de treino atual
        from treinos.models import PlanoTreino
        context['plano_atual'] = PlanoTreino.objects.filter(
            aluno=aluno,
            ativo=True
        ).first()
        
        # Próximas aulas
        from frequencia.models import AgendaAula
        context['proximas_aulas'] = AgendaAula.objects.filter(
            aluno=aluno,
            data_aula__gte=timezone.now().date(),
            status__in=['agendado', 'confirmado']
        ).order_by('data_aula', 'horario_inicio')[:3]
        
        # Faturas pendentes
        from financeiro.models import Fatura
        context['faturas_pendentes'] = Fatura.objects.filter(
            aluno=aluno,
            status__in=['pendente', 'parcial']
        ).order_by('data_vencimento')
        
        return context


@login_required
def adicionar_medidas(request, pk):
    """
    Adiciona novas medidas corporais para o aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    
    if request.method == 'POST':
        form = MedidasCorporaisForm(request.POST)
        if form.is_valid():
            medida = form.save(commit=False)
            medida.aluno = aluno
            medida.save()
            messages.success(request, 'Medidas corporais adicionadas com sucesso!')
            return redirect('alunos:detalhes', pk=pk)
    else:
        form = MedidasCorporaisForm()
    
    return render(request, 'alunos/adicionar_medidas.html', {
        'form': form,
        'aluno': aluno
    })


@login_required
def adicionar_foto(request, pk):
    """
    Adiciona foto de progresso para o aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    
    if request.method == 'POST':
        form = FotoProgressoForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.aluno = aluno
            foto.save()
            messages.success(request, 'Foto de progresso adicionada com sucesso!')
            return redirect('alunos:detalhes', pk=pk)
    else:
        form = FotoProgressoForm()
    
    return render(request, 'alunos/adicionar_foto.html', {
        'form': form,
        'aluno': aluno
    })


@login_required
def historico_medidas(request, pk):
    """
    Exibe histórico completo de medidas corporais do aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    medidas = MedidasCorporais.objects.filter(aluno=aluno).order_by('-data_medicao')
    
    return render(request, 'alunos/historico_medidas.html', {
        'aluno': aluno,
        'medidas': medidas
    })


@login_required
def galeria_fotos(request, pk):
    """
    Galeria com todas as fotos de progresso do aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    fotos = FotoProgresso.objects.filter(aluno=aluno).order_by('-data_foto')
    
    return render(request, 'alunos/galeria_fotos.html', {
        'aluno': aluno,
        'fotos': fotos
    })


@login_required
def toggle_status(request, pk):
    """
    Alterna status ativo/inativo do aluno via AJAX.
    """
    if request.method == 'POST':
        aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
        aluno.ativo = not aluno.ativo
        aluno.save()
        
        return JsonResponse({
            'success': True,
            'ativo': aluno.ativo,
            'status_text': 'Ativo' if aluno.ativo else 'Inativo'
        })
    
    return JsonResponse({'success': False})


@login_required
def estatisticas_aluno(request, pk):
    """
    Exibe estatísticas detalhadas do aluno.
    """
    aluno = get_object_or_404(Aluno, pk=pk, personal_trainer=request.user)
    
    # Evolução de peso (últimos 6 meses)
    seis_meses_atras = timezone.now() - timedelta(days=180)
    evolucao_peso = MedidasCorporais.objects.filter(
        aluno=aluno,
        data_medicao__gte=seis_meses_atras
    ).order_by('data_medicao').values('data_medicao', 'peso')
    
    # Frequência mensal
    from frequencia.models import RegistroPresenca
    frequencia_mensal = RegistroPresenca.objects.filter(
        aluno=aluno,
        presente=True
    ).extra(
        select={'mes': "DATE_FORMAT(data_presenca, '%%Y-%%m')"}
    ).values('mes').annotate(total=Count('id')).order_by('mes')
    
    context = {
        'aluno': aluno,
        'evolucao_peso': list(evolucao_peso),
        'frequencia_mensal': list(frequencia_mensal),
    }
    
    return render(request, 'alunos/estatisticas.html', context)
