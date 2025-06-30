"""
Views para gerenciamento de treinos e exercícios.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count
from django.http import JsonResponse

from .models import Exercicio, PlanoTreino, TreinoDiario, ExercicioTreino
from .forms import ExercicioForm, PlanoTreinoForm, TreinoDiarioForm, ExercicioTreinoForm
from alunos.models import Aluno


class ExercicioListView(LoginRequiredMixin, ListView):
    """
    Lista todos os exercícios disponíveis.
    """
    model = Exercicio
    template_name = 'treinos/exercicios.html'
    context_object_name = 'exercicios'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Exercicio.objects.all()
        
        # Filtros
        search = self.request.GET.get('search')
        grupo_muscular = self.request.GET.get('grupo_muscular')
        equipamento = self.request.GET.get('equipamento')
        
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(descricao__icontains=search)
            )
        
        if grupo_muscular:
            queryset = queryset.filter(grupo_muscular=grupo_muscular)
            
        if equipamento:
            queryset = queryset.filter(equipamento=equipamento)
        
        return queryset.order_by('grupo_muscular', 'nome')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['grupo_muscular'] = self.request.GET.get('grupo_muscular', '')
        context['equipamento'] = self.request.GET.get('equipamento', '')
        context['grupos_musculares'] = Exercicio.GRUPO_MUSCULAR_CHOICES
        context['equipamentos'] = Exercicio.EQUIPAMENTO_CHOICES
        return context


class PlanoTreinoListView(LoginRequiredMixin, ListView):
    """
    Lista todos os planos de treino do personal trainer.
    """
    model = PlanoTreino
    template_name = 'treinos/planos.html'
    context_object_name = 'planos'
    paginate_by = 20
    
    def get_queryset(self):
        return PlanoTreino.objects.filter(
            personal_trainer=self.request.user
        ).order_by('-data_criacao')


class PlanoTreinoCreateView(LoginRequiredMixin, CreateView):
    """
    Criação de novo plano de treino.
    """
    model = PlanoTreino
    form_class = PlanoTreinoForm
    template_name = 'treinos/criar_plano.html'
    success_url = reverse_lazy('treinos:planos')
    
    def form_valid(self, form):
        form.instance.personal_trainer = self.request.user
        messages.success(self.request, f'Plano de treino "{form.instance.nome}" criado com sucesso!')
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar apenas alunos do personal trainer logado
        form.fields['aluno'].queryset = Aluno.objects.filter(
            personal_trainer=self.request.user,
            ativo=True
        )
        return form


class PlanoTreinoDetailView(LoginRequiredMixin, DetailView):
    """
    Detalhes do plano de treino com seus dias e exercícios.
    """
    model = PlanoTreino
    template_name = 'treinos/detalhes_plano.html'
    context_object_name = 'plano'
    
    def get_queryset(self):
        return PlanoTreino.objects.filter(personal_trainer=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plano = self.object
        
        # Buscar dias de treino ordenados
        context['dias_treino'] = TreinoDiario.objects.filter(
            plano_treino=plano
        ).order_by('dia_semana')
        
        return context


@login_required
def criar_treino_diario(request, plano_id):
    """
    Adiciona um novo dia de treino ao plano.
    """
    plano = get_object_or_404(PlanoTreino, id=plano_id, personal_trainer=request.user)
    
    if request.method == 'POST':
        form = TreinoDiarioForm(request.POST)
        if form.is_valid():
            treino = form.save(commit=False)
            treino.plano_treino = plano
            treino.save()
            messages.success(request, 'Dia de treino adicionado com sucesso!')
            return redirect('treinos:detalhes_plano', pk=plano_id)
    else:
        form = TreinoDiarioForm()
    
    return render(request, 'treinos/criar_treino_diario.html', {
        'form': form,
        'plano': plano
    })


@login_required
def adicionar_exercicio_treino(request, treino_id):
    """
    Adiciona exercício a um dia de treino específico.
    """
    treino = get_object_or_404(TreinoDiario, id=treino_id, plano_treino__personal_trainer=request.user)
    
    if request.method == 'POST':
        form = ExercicioTreinoForm(request.POST)
        if form.is_valid():
            exercicio_treino = form.save(commit=False)
            exercicio_treino.treino_diario = treino
            exercicio_treino.save()
            messages.success(request, 'Exercício adicionado ao treino!')
            return redirect('treinos:detalhes_plano', pk=treino.plano_treino.id)
    else:
        form = ExercicioTreinoForm()
    
    return render(request, 'treinos/adicionar_exercicio.html', {
        'form': form,
        'treino': treino
    })


@login_required
def copiar_plano_treino(request, plano_id):
    """
    Copia um plano de treino existente.
    """
    plano_original = get_object_or_404(PlanoTreino, id=plano_id, personal_trainer=request.user)
    
    # Criar cópia do plano
    novo_plano = PlanoTreino.objects.create(
        nome=f"Cópia de {plano_original.nome}",
        descricao=plano_original.descricao,
        personal_trainer=request.user,
        ativo=False  # Criar inativo para edição
    )
    
    # Copiar dias de treino
    for dia_original in plano_original.dias_treino.all():
        novo_dia = TreinoDiario.objects.create(
            plano_treino=novo_plano,
            dia_semana=dia_original.dia_semana,
            nome=dia_original.nome,
            observacoes=dia_original.observacoes
        )
        
        # Copiar exercícios do dia
        for exercicio_original in dia_original.exercicios.all():
            ExercicioTreino.objects.create(
                treino_diario=novo_dia,
                exercicio=exercicio_original.exercicio,
                series=exercicio_original.series,
                repeticoes=exercicio_original.repeticoes,
                carga=exercicio_original.carga,
                tempo_descanso=exercicio_original.tempo_descanso,
                observacoes=exercicio_original.observacoes,
                ordem=exercicio_original.ordem
            )
    
    messages.success(request, f'Plano "{plano_original.nome}" copiado com sucesso!')
    return redirect('treinos:detalhes_plano', pk=novo_plano.id)


@login_required
def ativar_plano_treino(request, plano_id):
    """
    Ativa/desativa um plano de treino para um aluno.
    """
    if request.method == 'POST':
        plano = get_object_or_404(PlanoTreino, id=plano_id, personal_trainer=request.user)
        
        if plano.aluno:
            # Desativar outros planos do mesmo aluno
            PlanoTreino.objects.filter(
                aluno=plano.aluno,
                ativo=True
            ).exclude(id=plano_id).update(ativo=False)
            
            # Ativar este plano
            plano.ativo = not plano.ativo
            plano.save()
            
            status = "ativado" if plano.ativo else "desativado"
            messages.success(request, f'Plano "{plano.nome}" {status} com sucesso!')
        
        return JsonResponse({
            'success': True,
            'ativo': plano.ativo
        })
    
    return JsonResponse({'success': False})


class ExercicioCreateView(LoginRequiredMixin, CreateView):
    """
    Criação de novo exercício (apenas para admins).
    """
    model = Exercicio
    form_class = ExercicioForm
    template_name = 'treinos/criar_exercicio.html'
    success_url = reverse_lazy('treinos:exercicios')
    
    def form_valid(self, form):
        messages.success(self.request, f'Exercício "{form.instance.nome}" criado com sucesso!')
        return super().form_valid(form)
