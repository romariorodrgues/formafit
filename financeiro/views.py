"""
Views para gestão financeira.
"""
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from decimal import Decimal
import json

from .models import PlanoMensalidade, ContratoAluno, Fatura, Pagamento
from .forms import PlanoMensalidadeForm, ContratoAlunoForm, FaturaForm, PagamentoForm, FiltroFinanceiroForm
from .services import FinanceiroService
from alunos.models import Aluno

@login_required
def dashboard_financeiro(request):
    """Dashboard financeiro completo."""
    service = FinanceiroService()
    
    # Período atual (mês atual)
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    # Estatísticas gerais
    stats_gerais = service.calcular_estatisticas_financeiras(request.user)
    stats_mes = service.calcular_estatisticas_financeiras(request.user, mes_atual, ano_atual)
    
    # Faturas recentes
    faturas_recentes = Fatura.objects.filter(
        aluno__personal_trainer=request.user
    ).select_related('aluno', 'contrato').order_by('-data_criacao')[:10]
    
    # Faturas atrasadas
    faturas_atrasadas = Fatura.objects.filter(
        aluno__personal_trainer=request.user,
        status='atrasada'
    ).select_related('aluno').order_by('data_vencimento')[:5]
    
    # Pagamentos recentes
    pagamentos_recentes = Pagamento.objects.filter(
        fatura__aluno__personal_trainer=request.user
    ).select_related('fatura', 'fatura__aluno').order_by('-data_pagamento')[:10]
    
    # Alunos com contratos ativos
    contratos_ativos = ContratoAluno.objects.filter(
        aluno__personal_trainer=request.user,
        ativo=True
    ).count()
    
    # Receita por forma de pagamento (últimos 30 dias)
    data_limite = hoje - timedelta(days=30)
    receita_forma_pagamento = Pagamento.objects.filter(
        fatura__aluno__personal_trainer=request.user,
        data_pagamento__gte=data_limite
    ).values('forma_pagamento').annotate(
        total=Sum('valor_pago'),
        count=Count('id')
    ).order_by('-total')
    
    # Receitas dos últimos 6 meses para o gráfico
    receitas_ultimos_meses = []
    for i in range(5, -1, -1):  # 6 meses atrás até o mês atual
        mes_calc = hoje.month - i
        ano_calc = hoje.year
        
        # Ajustar ano se o mês for menor que 1
        if mes_calc <= 0:
            mes_calc += 12
            ano_calc -= 1
        
        receita_mes = Pagamento.objects.filter(
            fatura__aluno__personal_trainer=request.user,
            data_pagamento__month=mes_calc,
            data_pagamento__year=ano_calc
        ).aggregate(total=Sum('valor_pago'))['total'] or 0
        
        receitas_ultimos_meses.append(float(receita_mes))
    
    context = {
        'stats_gerais': stats_gerais,
        'stats_mes': stats_mes,
        'faturas_recentes': faturas_recentes,
        'faturas_atrasadas': faturas_atrasadas,
        'pagamentos_recentes': pagamentos_recentes,
        'contratos_ativos': contratos_ativos,
        'receita_forma_pagamento': receita_forma_pagamento,
        'receitas_ultimos_meses': receitas_ultimos_meses,
        'mes_atual': mes_atual,
        'ano_atual': ano_atual,
    }
    
    return render(request, 'financeiro/dashboard.html', context)


@login_required
def lista_faturas(request):
    """Lista de faturas com filtros."""
    filtro_form = FiltroFinanceiroForm(request.user, request.GET)
    
    # Queryset base
    faturas = Fatura.objects.filter(
        aluno__personal_trainer=request.user
    ).select_related('aluno', 'contrato').order_by('-ano_referencia', '-mes_referencia')
    
    # Aplicar filtros
    if filtro_form.is_valid():
        if filtro_form.cleaned_data['aluno']:
            faturas = faturas.filter(aluno=filtro_form.cleaned_data['aluno'])
        
        if filtro_form.cleaned_data['status']:
            faturas = faturas.filter(status=filtro_form.cleaned_data['status'])
        
        if filtro_form.cleaned_data['mes']:
            faturas = faturas.filter(mes_referencia=filtro_form.cleaned_data['mes'])
        
        if filtro_form.cleaned_data['ano']:
            faturas = faturas.filter(ano_referencia=filtro_form.cleaned_data['ano'])
        
        # TODO: Adicionar campos de data no formulário se necessário
        # if filtro_form.cleaned_data.get('data_vencimento_inicio'):
        #     faturas = faturas.filter(data_vencimento__gte=filtro_form.cleaned_data['data_vencimento_inicio'])
        # 
        # if filtro_form.cleaned_data.get('data_vencimento_fim'):
        #     faturas = faturas.filter(data_vencimento__lte=filtro_form.cleaned_data['data_vencimento_fim'])
    
    # Atualizar status das faturas
    service = FinanceiroService()
    service.atualizar_status_faturas()
    
    # Estatísticas da lista filtrada
    total_faturas = faturas.count()
    valor_total = faturas.aggregate(total=Sum('valor_final'))['total'] or Decimal('0.00')
    faturas_pagas = faturas.filter(status='paga').count()
    faturas_pendentes = faturas.filter(status__in=['pendente', 'atrasada']).count()
    
    context = {
        'faturas': faturas,
        'filtro_form': filtro_form,
        'total_faturas': total_faturas,
        'valor_total': valor_total,
        'faturas_pagas': faturas_pagas,
        'faturas_pendentes': faturas_pendentes,
    }
    
    return render(request, 'financeiro/lista_faturas.html', context)


@login_required
def fatura_detail(request, pk):
    """Detalhes de uma fatura."""
    fatura = get_object_or_404(
        Fatura,
        pk=pk,
        aluno__personal_trainer=request.user
    )
    
    # Pagamentos da fatura
    pagamentos = fatura.pagamentos.order_by('-data_pagamento')
    total_pago = pagamentos.aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
    saldo_devedor = fatura.valor_final - total_pago
    
    context = {
        'fatura': fatura,
        'pagamentos': pagamentos,
        'total_pago': total_pago,
        'saldo_devedor': saldo_devedor,
        'pode_pagar': saldo_devedor > 0,
    }
    
    return render(request, 'financeiro/fatura_detail.html', context)


@login_required
def criar_fatura(request):
    """Criar nova fatura."""
    if request.method == 'POST':
        form = FaturaForm(request.POST, user=request.user)
        if form.is_valid():
            fatura = form.save(commit=False)
            
            # Buscar contrato do aluno
            try:
                contrato = ContratoAluno.objects.get(
                    aluno=fatura.aluno,
                    ativo=True
                )
                fatura.contrato = contrato
            except ContratoAluno.DoesNotExist:
                messages.error(request, 'Aluno não possui contrato ativo.')
                return render(request, 'financeiro/criar_fatura.html', {'form': form})
            
            fatura.save()
            messages.success(request, f'Fatura criada com sucesso!')
            return redirect('financeiro:fatura_detail', pk=fatura.pk)
    else:
        form = FaturaForm(user=request.user)
    
    return render(request, 'financeiro/criar_fatura.html', {'form': form})


@login_required
def gerar_faturas_automaticas(request):
    """Gerar faturas automáticas para o mês atual."""
    if request.method == 'POST':
        mes = int(request.POST.get('mes', timezone.now().month))
        ano = int(request.POST.get('ano', timezone.now().year))
        
        service = FinanceiroService()
        faturas_criadas = service.gerar_faturas_automaticas(mes, ano, request.user)
        
        if faturas_criadas:
            messages.success(
                request, 
                f'{len(faturas_criadas)} fatura(s) criada(s) para {mes:02d}/{ano}!'
            )
        else:
            messages.info(request, 'Todas as faturas já foram geradas para este período.')
        
        return redirect('financeiro:lista_faturas')
    
    context = {
        'mes_atual': timezone.now().month,
        'ano_atual': timezone.now().year,
    }
    
    return render(request, 'financeiro/gerar_faturas.html', context)


@login_required
def registrar_pagamento(request, fatura_id):
    """Registrar pagamento de uma fatura."""
    fatura = get_object_or_404(
        Fatura,
        pk=fatura_id,
        aluno__personal_trainer=request.user
    )
    
    if request.method == 'POST':
        form = PagamentoForm(request.POST, user=request.user)
        if form.is_valid():
            pagamento = form.save()
            
            # Atualizar status da fatura usando o serviço
            service = FinanceiroService()
            service.registrar_pagamento(
                fatura=pagamento.fatura,
                valor_pago=pagamento.valor_pago,
                data_pagamento=pagamento.data_pagamento,
                forma_pagamento=pagamento.forma_pagamento,
                observacoes=pagamento.observacoes
            )
            
            messages.success(request, 'Pagamento registrado com sucesso!')
            return redirect('financeiro:fatura_detail', pk=fatura.pk)
    else:
        form = PagamentoForm(user=request.user, initial={'fatura': fatura})
    
    context = {
        'form': form,
        'fatura': fatura,
    }
    
    return render(request, 'financeiro/registrar_pagamento.html', context)


@login_required
def lista_contratos(request):
    """Lista de contratos."""
    contratos = ContratoAluno.objects.filter(
        aluno__personal_trainer=request.user
    ).select_related('aluno', 'plano_mensalidade').order_by('-data_inicio')
    
    context = {
        'contratos': contratos,
    }
    
    return render(request, 'financeiro/contratos.html', context)


@login_required
def criar_contrato(request):
    """Criar novo contrato."""
    if request.method == 'POST':
        form = ContratoAlunoForm(request.POST, user=request.user)
        if form.is_valid():
            contrato = form.save()
            messages.success(request, f'Contrato criado para {contrato.aluno.nome}!')
            return redirect('financeiro:lista_contratos')
    else:
        form = ContratoAlunoForm(user=request.user)
    
    return render(request, 'financeiro/criar_contrato.html', {'form': form})


@login_required
def lista_planos(request):
    """Lista de planos de mensalidade."""
    planos = PlanoMensalidade.objects.all().order_by('valor')
    
    context = {
        'planos': planos,
    }
    
    return render(request, 'financeiro/lista_planos.html', context)


@login_required
def criar_plano(request):
    """Criar um novo plano de mensalidade."""
    if request.method == 'POST':
        form = PlanoMensalidadeForm(request.POST)
        if form.is_valid():
            plano = form.save()
            messages.success(request, f'Plano "{plano.nome}" criado com sucesso!')
            return redirect('financeiro:lista_planos')
    else:
        form = PlanoMensalidadeForm()
    
    return render(request, 'financeiro/criar_plano.html', {'form': form})


@login_required
def editar_plano(request, pk):
    """Editar plano de mensalidade."""
    plano = get_object_or_404(PlanoMensalidade, pk=pk)
    
    if request.method == 'POST':
        form = PlanoMensalidadeForm(request.POST, instance=plano)
        if form.is_valid():
            plano = form.save()
            messages.success(request, f'Plano "{plano.nome}" atualizado com sucesso!')
            return redirect('financeiro:lista_planos')
    else:
        form = PlanoMensalidadeForm(instance=plano)
    
    return render(request, 'financeiro/editar_plano.html', {
        'form': form,
        'plano': plano
    })


@login_required
def deletar_plano(request, pk):
    """Deletar plano de mensalidade."""
    plano = get_object_or_404(PlanoMensalidade, pk=pk)
    
    # Verificar se há contratos vinculados
    contratos_vinculados = ContratoAluno.objects.filter(plano_mensalidade=plano).count()
    
    if contratos_vinculados > 0:
        messages.error(
            request, 
            f'Não é possível excluir o plano "{plano.nome}" pois há {contratos_vinculados} contratos vinculados a ele.'
        )
        return redirect('financeiro:lista_planos')
    
    if request.method == 'POST':
        nome_plano = plano.nome
        plano.delete()
        messages.success(request, f'Plano "{nome_plano}" excluído com sucesso!')
        return redirect('financeiro:lista_planos')
    
    return redirect('financeiro:editar_plano', pk=pk)


@login_required
def relatorio_financeiro(request):
    """Gerar relatório financeiro."""
    # Filtros de período
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if data_inicio:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    else:
        # Período padrão (último mês)
        hoje = timezone.now().date()
        data_inicio = hoje.replace(day=1)
    
    if data_fim:
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    else:
        hoje = timezone.now().date()
        data_fim = hoje
    
    # Gerar relatório usando o service
    service = FinanceiroService()
    relatorio = service.gerar_relatorio_periodo(request.user, data_inicio, data_fim)
    
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'relatorio': relatorio,
    }
    
    return render(request, 'financeiro/relatorio_financeiro.html', context)


@login_required
def inadimplencia_view(request):
    """Relatório de inadimplência."""
    from django.core.paginator import Paginator
    
    # Filtros
    dias_atraso = request.GET.get('dias_atraso')
    valor_minimo = request.GET.get('valor_minimo')
    ordenar = request.GET.get('ordenar', 'dias_atraso')
    
    # Query base - faturas vencidas
    hoje = timezone.now().date()
    faturas_vencidas = Fatura.objects.filter(
        contrato__aluno__personal_trainer=request.user,
        status='pendente',
        data_vencimento__lt=hoje
    ).select_related('contrato__aluno', 'contrato__plano_mensalidade')
    
    # Aplicar filtros
    if dias_atraso:
        data_limite = hoje - timedelta(days=int(dias_atraso))
        faturas_vencidas = faturas_vencidas.filter(data_vencimento__lte=data_limite)
    
    if valor_minimo:
        faturas_vencidas = faturas_vencidas.filter(valor_final__gte=valor_minimo)
    
    # Adicionar campo calculado de dias de atraso
    for fatura in faturas_vencidas:
        fatura.dias_atraso = (hoje - fatura.data_vencimento).days
    
    # Ordenação
    if ordenar == 'dias_atraso':
        faturas_vencidas = sorted(faturas_vencidas, key=lambda f: f.dias_atraso, reverse=True)
    elif ordenar == 'valor':
        faturas_vencidas = faturas_vencidas.order_by('-valor_final')
    elif ordenar == 'vencimento':
        faturas_vencidas = faturas_vencidas.order_by('data_vencimento')
    elif ordenar == 'aluno':
        faturas_vencidas = faturas_vencidas.order_by('contrato__aluno__nome')
    
    # Paginação
    paginator = Paginator(faturas_vencidas, 20)
    page_number = request.GET.get('page')
    faturas_vencidas = paginator.get_page(page_number)
    
    # Estatísticas resumo
    todas_faturas = Fatura.objects.filter(contrato__aluno__personal_trainer=request.user)
    total_faturas = todas_faturas.count()
    total_vencidas = todas_faturas.filter(
        status='pendente',
        data_vencimento__lt=hoje
    ).count()
    
    total_em_atraso = todas_faturas.filter(
        status='pendente',
        data_vencimento__lt=hoje
    ).aggregate(total=Sum('valor_final'))['total'] or Decimal('0.00')
    
    clientes_inadimplentes = todas_faturas.filter(
        status='pendente',
        data_vencimento__lt=hoje
    ).values('contrato__aluno').distinct().count()
    
    total_clientes = ContratoAluno.objects.filter(
        aluno__personal_trainer=request.user,
        ativo=True
    ).count()
    
    taxa_inadimplencia = (total_vencidas / max(total_faturas, 1)) * 100
    
    # Calcular média de dias em atraso
    faturas_com_atraso = todas_faturas.filter(
        status='pendente',
        data_vencimento__lt=hoje
    )
    
    total_dias_atraso = sum((hoje - f.data_vencimento).days for f in faturas_com_atraso)
    media_dias_atraso = total_dias_atraso // max(faturas_com_atraso.count(), 1)
    
    resumo = {
        'total_em_atraso': total_em_atraso,
        'faturas_vencidas': total_vencidas,
        'clientes_inadimplentes': clientes_inadimplentes,
        'total_clientes': total_clientes,
        'taxa_inadimplencia': round(taxa_inadimplencia, 2),
        'media_dias_atraso': media_dias_atraso,
    }
    
    context = {
        'faturas_vencidas': faturas_vencidas,
        'resumo': resumo,
    }
    
    return render(request, 'financeiro/inadimplencia.html', context)


@login_required
def contrato_detail(request, pk):
    """Detalhe do contrato."""
    contrato = get_object_or_404(ContratoAluno, pk=pk, aluno__personal_trainer=request.user)
    
    # Faturas do contrato
    faturas = Fatura.objects.filter(contrato=contrato).order_by('-ano_referencia', '-mes_referencia')
    
    context = {
        'contrato': contrato,
        'faturas': faturas,
    }
    
    return render(request, 'financeiro/contrato_detail.html', context)


# Views AJAX adicionais
@login_required
def ajax_update_contrato(request, pk):
    """Atualizar contrato via AJAX."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        contrato = get_object_or_404(ContratoAluno, pk=pk, aluno__personal_trainer=request.user)
        
        # Aqui você pode adicionar lógica para atualizar o contrato
        # Por exemplo, ativar/desativar
        ativo = request.POST.get('ativo') == 'true'
        contrato.ativo = ativo
        contrato.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Contrato atualizado com sucesso!',
            'contrato': {
                'id': contrato.id,
                'ativo': contrato.ativo,
                'aluno_nome': contrato.aluno.nome,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def ajax_plano_details(request, pk):
    """Detalhes do plano via AJAX."""
    try:
        plano = get_object_or_404(PlanoMensalidade, pk=pk)
        
        return JsonResponse({
            'success': True,
            'plano': {
                'id': plano.id,
                'nome': plano.nome,
                'valor': float(plano.valor),
                'aulas_incluidas': plano.aulas_incluidas,
                'descricao': plano.descricao,
                'ativo': plano.ativo,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def ajax_delete_plano(request, pk):
    """Deletar plano via AJAX."""
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        plano = get_object_or_404(PlanoMensalidade, pk=pk)
        
        # Verificar se há contratos usando este plano
        contratos_ativos = ContratoAluno.objects.filter(plano_mensalidade=plano, ativo=True)
        if contratos_ativos.exists():
            return JsonResponse({
                'error': 'Não é possível excluir este plano pois há contratos ativos vinculados.'
            }, status=400)
        
        nome_plano = plano.nome
        plano.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Plano "{nome_plano}" excluído com sucesso!'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# AJAX Views
@login_required
def ajax_estatisticas_mes(request):
    """Retorna estatísticas do mês via AJAX."""
    mes = int(request.GET.get('mes', timezone.now().month))
    ano = int(request.GET.get('ano', timezone.now().year))
    
    service = FinanceiroService()
    stats = service.calcular_estatisticas_financeiras(request.user, mes, ano)
    
    return JsonResponse(stats, safe=False)


@login_required
def ajax_dados_grafico_receita(request):
    """Retorna dados para gráfico de receita via AJAX."""
    # Últimos 12 meses
    hoje = timezone.now().date()
    data_inicio = hoje.replace(day=1) - timedelta(days=365)
    
    pagamentos = Pagamento.objects.filter(
        fatura__aluno__personal_trainer=request.user,
        data_pagamento__gte=data_inicio,
        data_pagamento__lte=hoje
    ).values('data_pagamento__year', 'data_pagamento__month').annotate(
        total=Sum('valor_pago')
    ).order_by('data_pagamento__year', 'data_pagamento__month')
    
    dados = []
    for p in pagamentos:
        dados.append({
            'mes': f"{p['data_pagamento__month']:02d}/{p['data_pagamento__year']}",
            'valor': float(p['total'])
        })
    
    return JsonResponse(dados, safe=False)
