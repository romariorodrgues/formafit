"""
Serviços para operações financeiras.
"""
import os
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum, Count, Q, Avg
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from io import BytesIO
import base64

from .models import PlanoMensalidade, ContratoAluno, Fatura, Pagamento
from alunos.models import Aluno


class FinanceiroService:
    """Serviço para operações financeiras."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos customizados para PDFs."""
        self.titulo_style = ParagraphStyle(
            'TituloCustom',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=HexColor('#2563eb'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        self.subtitulo_style = ParagraphStyle(
            'SubtituloCustom',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#374151'),
            alignment=TA_LEFT,
            spaceBefore=15,
            spaceAfter=10
        )
        
        self.texto_style = ParagraphStyle(
            'TextoCustom',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=HexColor('#4b5563'),
            alignment=TA_LEFT,
            spaceAfter=8
        )
    
    def gerar_faturas_automaticas(self, mes, ano, personal_trainer):
        """Gera faturas automáticas para um mês específico."""
        faturas_criadas = []
        
        # Buscar contratos ativos
        contratos = ContratoAluno.objects.filter(
            aluno__personal_trainer=personal_trainer,
            ativo=True,
            data_inicio__lte=timezone.now().date()
        ).filter(
            Q(data_fim__isnull=True) | Q(data_fim__gte=timezone.now().date())
        )
        
        for contrato in contratos:
            # Verificar se já existe fatura para o período
            fatura_existente = Fatura.objects.filter(
                aluno=contrato.aluno,
                mes_referencia=mes,
                ano_referencia=ano
            ).exists()
            
            if not fatura_existente:
                # Calcular data de vencimento
                try:
                    data_vencimento = datetime(ano, mes, contrato.dia_vencimento).date()
                except ValueError:
                    # Caso o dia não exista no mês (ex: 31 de fevereiro)
                    data_vencimento = datetime(ano, mes, 28).date()
                
                # Criar fatura
                fatura = Fatura.objects.create(
                    aluno=contrato.aluno,
                    contrato=contrato,
                    mes_referencia=mes,
                    ano_referencia=ano,
                    valor_original=contrato.valor_mensalidade,
                    data_vencimento=data_vencimento,
                    status='pendente'
                )
                
                faturas_criadas.append(fatura)
        
        return faturas_criadas
    
    def atualizar_status_faturas(self):
        """Atualiza status das faturas baseado na data de vencimento."""
        hoje = timezone.now().date()
        
        # Marcar como atrasadas
        faturas_atrasadas = Fatura.objects.filter(
            status='pendente',
            data_vencimento__lt=hoje
        )
        faturas_atrasadas.update(status='atrasada')
        
        return faturas_atrasadas.count()
    
    def calcular_estatisticas_financeiras(self, personal_trainer, mes=None, ano=None):
        """Calcula estatísticas financeiras do personal trainer."""
        # Filtros base
        faturas_qs = Fatura.objects.filter(aluno__personal_trainer=personal_trainer)
        pagamentos_qs = Pagamento.objects.filter(fatura__aluno__personal_trainer=personal_trainer)
        
        if mes and ano:
            faturas_qs = faturas_qs.filter(mes_referencia=mes, ano_referencia=ano)
            pagamentos_qs = pagamentos_qs.filter(
                fatura__mes_referencia=mes,
                fatura__ano_referencia=ano
            )
        
        # Receita total
        receita_total = pagamentos_qs.aggregate(
            total=Sum('valor_pago')
        )['total'] or Decimal('0.00')
        
        # Faturas pendentes
        valor_pendente = faturas_qs.filter(
            status__in=['pendente', 'atrasada']
        ).aggregate(
            total=Sum('valor_final')
        )['total'] or Decimal('0.00')
        
        # Faturas pagas
        valor_recebido = faturas_qs.filter(
            status='paga'
        ).aggregate(
            total=Sum('valor_final')
        )['total'] or Decimal('0.00')
        
        # Inadimplência
        faturas_atrasadas = faturas_qs.filter(status='atrasada').count()
        total_faturas = faturas_qs.count()
        percentual_inadimplencia = (faturas_atrasadas / max(total_faturas, 1)) * 100
        
        # Ticket médio
        ticket_medio = faturas_qs.aggregate(
            media=Avg('valor_final')
        )['media'] or Decimal('0.00')
        
        return {
            'receita_total': receita_total,
            'valor_pendente': valor_pendente,
            'valor_recebido': valor_recebido,
            'faturas_atrasadas': faturas_atrasadas,
            'total_faturas': total_faturas,
            'percentual_inadimplencia': round(percentual_inadimplencia, 2),
            'ticket_medio': ticket_medio,
        }
    
    def gerar_relatorio_financeiro(self, personal_trainer, periodo_inicio, periodo_fim):
        """Gera relatório financeiro em PDF."""
        # Coletar dados
        dados = self._coletar_dados_financeiros(personal_trainer, periodo_inicio, periodo_fim)
        
        # Gerar gráficos
        graficos = self._gerar_graficos_financeiros(dados)
        
        # Criar PDF
        filename = f"relatorio_financeiro_{periodo_inicio}_{periodo_fim}.pdf"
        filepath = os.path.join(settings.MEDIA_ROOT, 'relatorios_financeiros', filename)
        
        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Criar PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Cabeçalho
        story.append(Paragraph("Relatório Financeiro", self.titulo_style))
        story.append(Paragraph(f"Período: {periodo_inicio.strftime('%d/%m/%Y')} a {periodo_fim.strftime('%d/%m/%Y')}", self.subtitulo_style))
        story.append(Spacer(1, 20))
        
        # Resumo financeiro
        story.append(Paragraph("Resumo Financeiro", self.subtitulo_style))
        
        resumo_data = [
            ['Receita Total', f"R$ {dados['estatisticas']['receita_total']:.2f}"],
            ['Valor Recebido', f"R$ {dados['estatisticas']['valor_recebido']:.2f}"],
            ['Valor Pendente', f"R$ {dados['estatisticas']['valor_pendente']:.2f}"],
            ['Faturas Atrasadas', f"{dados['estatisticas']['faturas_atrasadas']}"],
            ['% Inadimplência', f"{dados['estatisticas']['percentual_inadimplencia']:.1f}%"],
            ['Ticket Médio', f"R$ {dados['estatisticas']['ticket_medio']:.2f}"],
        ]
        
        resumo_table = Table(resumo_data, colWidths=[8*cm, 8*cm])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(resumo_table)
        story.append(Spacer(1, 30))
        
        # Construir PDF
        doc.build(story)
        
        return f"relatorios_financeiros/{filename}"
    
    def _coletar_dados_financeiros(self, personal_trainer, periodo_inicio, periodo_fim):
        """Coleta dados financeiros para relatório."""
        # Faturas no período
        faturas = Fatura.objects.filter(
            aluno__personal_trainer=personal_trainer,
            data_vencimento__gte=periodo_inicio,
            data_vencimento__lte=periodo_fim
        ).select_related('aluno', 'contrato')
        
        # Pagamentos no período
        pagamentos = Pagamento.objects.filter(
            fatura__aluno__personal_trainer=personal_trainer,
            data_pagamento__gte=periodo_inicio,
            data_pagamento__lte=periodo_fim
        ).select_related('fatura', 'fatura__aluno')
        
        # Estatísticas
        estatisticas = self.calcular_estatisticas_financeiras(
            personal_trainer,
            mes=periodo_inicio.month if periodo_inicio.month == periodo_fim.month else None,
            ano=periodo_inicio.year if periodo_inicio.year == periodo_fim.year else None
        )
        
        return {
            'faturas': list(faturas),
            'pagamentos': list(pagamentos),
            'estatisticas': estatisticas,
            'periodo_inicio': periodo_inicio,
            'periodo_fim': periodo_fim,
        }
    
    def _gerar_graficos_financeiros(self, dados):
        """Gera gráficos para relatório financeiro."""
        graficos = {}
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Gráfico de receita por mês
        if dados['pagamentos']:
            graficos['receita_mensal'] = self._criar_grafico_receita_mensal(dados['pagamentos'])
        
        # Gráfico de status das faturas
        if dados['faturas']:
            graficos['status_faturas'] = self._criar_grafico_status_faturas(dados['faturas'])
        
        return graficos
    
    def _criar_grafico_receita_mensal(self, pagamentos):
        """Cria gráfico de receita mensal."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Organizar dados por mês
        df_pagamentos = pd.DataFrame([{
            'data': p.data_pagamento,
            'valor': float(p.valor_pago)
        } for p in pagamentos])
        
        if not df_pagamentos.empty:
            df_pagamentos['data'] = pd.to_datetime(df_pagamentos['data'])
            df_pagamentos['mes'] = df_pagamentos['data'].dt.to_period('M')
            
            receita_mensal = df_pagamentos.groupby('mes')['valor'].sum()
            
            meses = [str(m) for m in receita_mensal.index]
            valores = receita_mensal.values
            
            bars = ax.bar(meses, valores, color='#2563eb', alpha=0.8)
            
            # Adicionar valores nas barras
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'R$ {height:.0f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom',
                           fontweight='bold')
        
        ax.set_title('Receita Mensal', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Mês', fontsize=12)
        ax.set_ylabel('Receita (R$)', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Salvar como base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        grafico_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return grafico_base64
    
    def _criar_grafico_status_faturas(self, faturas):
        """Cria gráfico de status das faturas."""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Contar status
        status_count = {}
        status_labels = {
            'pendente': 'Pendente',
            'paga': 'Paga',
            'atrasada': 'Atrasada',
            'cancelada': 'Cancelada',
            'parcial': 'Parcial'
        }
        
        for fatura in faturas:
            status = fatura.status
            if status not in status_count:
                status_count[status] = 0
            status_count[status] += 1
        
        if status_count:
            labels = [status_labels.get(k, k) for k in status_count.keys()]
            sizes = list(status_count.values())
            colors = ['#10b981', '#f59e0b', '#ef4444', '#6b7280', '#8b5cf6']
            
            ax.pie(sizes, labels=labels, colors=colors[:len(sizes)], autopct='%1.1f%%', startangle=90)
            ax.set_title('Status das Faturas', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Salvar como base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        grafico_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return grafico_base64
    
    def registrar_pagamento(self, fatura, valor_pago, data_pagamento, forma_pagamento, observacoes=''):
        """Registra um pagamento e atualiza status da fatura."""
        # Criar pagamento
        pagamento = Pagamento.objects.create(
            fatura=fatura,
            valor_pago=valor_pago,
            data_pagamento=data_pagamento,
            forma_pagamento=forma_pagamento,
            observacoes=observacoes
        )
        
        # Calcular total pago
        total_pago = fatura.pagamentos.aggregate(
            total=Sum('valor_pago')
        )['total'] or Decimal('0.00')
        
        # Atualizar status da fatura
        if total_pago >= fatura.valor_final:
            fatura.status = 'paga'
        elif total_pago > 0:
            fatura.status = 'parcial'
        
        fatura.save()
        
        return pagamento
    
    def gerar_relatorio_periodo(self, personal_trainer, data_inicio, data_fim):
        """Gera relatório financeiro para um período específico."""
        # Filtros base
        faturas_qs = Fatura.objects.filter(
            contrato__aluno__personal_trainer=personal_trainer,
            data_vencimento__gte=data_inicio,
            data_vencimento__lte=data_fim
        ).select_related('contrato__aluno', 'contrato__plano_mensalidade')
        
        pagamentos_qs = Pagamento.objects.filter(
            fatura__contrato__aluno__personal_trainer=personal_trainer,
            data_pagamento__gte=data_inicio,
            data_pagamento__lte=data_fim
        )
        
        # Calcular estatísticas
        receita_total = pagamentos_qs.aggregate(
            total=Sum('valor_pago')
        )['total'] or Decimal('0.00')
        
        faturas_pagas = faturas_qs.filter(status='paga').count()
        faturas_pendentes = faturas_qs.filter(status='pendente').count()
        faturas_vencidas = faturas_qs.filter(
            status='pendente',
            data_vencimento__lt=timezone.now().date()
        ).count()
        
        receita_pendente = faturas_qs.filter(
            status='pendente'
        ).aggregate(total=Sum('valor_final'))['total'] or Decimal('0.00')
        
        total_faturas = faturas_qs.count()
        taxa_inadimplencia = (faturas_vencidas / max(total_faturas, 1)) * 100
        
        # Receita por plano
        receita_por_plano = []
        planos = PlanoMensalidade.objects.filter(
            contratoaluno__aluno__personal_trainer=personal_trainer
        ).distinct()
        
        for plano in planos:
            contratos_ativos = ContratoAluno.objects.filter(
                aluno__personal_trainer=personal_trainer,
                plano_mensalidade=plano,
                ativo=True
            ).count()
            
            receita_plano = pagamentos_qs.filter(
                fatura__contrato__plano_mensalidade=plano
            ).aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
            
            pendente_plano = faturas_qs.filter(
                contrato__plano_mensalidade=plano,
                status='pendente'
            ).aggregate(total=Sum('valor_final'))['total'] or Decimal('0.00')
            
            total_plano = receita_plano + pendente_plano
            taxa_pagamento = (receita_plano / max(total_plano, 1)) * 100
            
            receita_por_plano.append({
                'nome': plano.nome,
                'contratos_ativos': contratos_ativos,
                'receita_total': receita_plano,
                'receita_pendente': pendente_plano,
                'taxa_pagamento': round(taxa_pagamento, 1)
            })
        
        # Últimas faturas
        ultimas_faturas = faturas_qs.order_by('-data_vencimento')[:10]
        
        # Dados para gráfico (últimos 6 meses)
        labels_meses = []
        dados_receita = []
        
        mes_atual = data_fim.month
        ano_atual = data_fim.year
        
        for i in range(5, -1, -1):
            mes_calc = mes_atual - i
            ano_calc = ano_atual
            
            if mes_calc <= 0:
                mes_calc += 12
                ano_calc -= 1
            
            receita_mes = pagamentos_qs.filter(
                data_pagamento__month=mes_calc,
                data_pagamento__year=ano_calc
            ).aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
            
            labels_meses.append(f"{mes_calc:02d}/{ano_calc}")
            dados_receita.append(float(receita_mes))
        
        return {
            'receita_total': receita_total,
            'receita_pendente': receita_pendente,
            'faturas_pagas': faturas_pagas,
            'faturas_pendentes': faturas_pendentes,
            'faturas_vencidas': faturas_vencidas,
            'taxa_inadimplencia': round(taxa_inadimplencia, 2),
            'receita_por_plano': receita_por_plano,
            'ultimas_faturas': ultimas_faturas,
            'labels_meses': labels_meses,
            'dados_receita': dados_receita,
        }
