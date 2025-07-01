"""
Serviços para geração de relatórios e gráficos.
"""
import os
import io
import base64
from datetime import datetime, timedelta
from decimal import Decimal
from django.conf import settings
from django.template.loader import get_template
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Avg, Count, Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from io import BytesIO

from .models import RelatorioProgresso, TipoRelatorio
from alunos.models import Aluno, MedidasCorporais
from frequencia.models import RegistroPresenca


class RelatorioService:
    """Serviço para geração de relatórios de progresso."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos customizados para o PDF."""
        # Título principal
        self.titulo_style = ParagraphStyle(
            'TituloCustom',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=HexColor('#2563eb'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        # Subtítulo
        self.subtitulo_style = ParagraphStyle(
            'SubtituloCustom',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#374151'),
            alignment=TA_LEFT,
            spaceBefore=15,
            spaceAfter=10
        )
        
        # Texto normal
        self.texto_style = ParagraphStyle(
            'TextoCustom',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=HexColor('#4b5563'),
            alignment=TA_LEFT,
            spaceAfter=8
        )
        
        # Destaque
        self.destaque_style = ParagraphStyle(
            'DestaqueCustom',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=HexColor('#059669'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=10
        )
    
    def gerar_relatorio_progresso(self, relatorio_id):
        """Gera um relatório de progresso em PDF."""
        try:
            relatorio = RelatorioProgresso.objects.get(id=relatorio_id)
            
            # Atualizar status
            relatorio.status = 'gerando'
            relatorio.save()
            
            # Coletar dados
            dados = self._coletar_dados_relatorio(relatorio)
            
            # Gerar gráficos
            graficos = self._gerar_graficos(relatorio, dados)
            
            # Criar PDF
            pdf_path = self._criar_pdf(relatorio, dados, graficos)
            
            # Atualizar relatório
            relatorio.arquivo_pdf = pdf_path
            relatorio.status = 'concluido'
            
            # Calcular estatísticas
            self._calcular_estatisticas(relatorio, dados)
            
            relatorio.save()
            
            return relatorio
            
        except Exception as e:
            if 'relatorio' in locals():
                relatorio.status = 'erro'
                relatorio.save()
            raise e
    
    def _coletar_dados_relatorio(self, relatorio):
        """Coleta todos os dados necessários para o relatório."""
        aluno = relatorio.aluno
        data_inicio = relatorio.data_inicio
        data_fim = relatorio.data_fim
        
        dados = {
            'aluno': aluno,
            'periodo': f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}",
            'medidas': [],
            'presencas': [],
            'estatisticas': {}
        }
        
        # Medidas corporais no período
        medidas = MedidasCorporais.objects.filter(
            aluno=aluno,
            data_medicao__gte=data_inicio,
            data_medicao__lte=data_fim
        ).order_by('data_medicao')
        
        dados['medidas'] = list(medidas)
        
        # Presenças no período
        presencas = RegistroPresenca.objects.filter(
            aluno=aluno,
            data_aula__gte=data_inicio,
            data_aula__lte=data_fim,
            status='presente'
        ).order_by('data_aula')
        
        dados['presencas'] = list(presencas)
        
        # Estatísticas básicas
        total_dias = (data_fim - data_inicio).days + 1
        total_presencas = len(dados['presencas'])
        
        dados['estatisticas'] = {
            'total_dias': total_dias,
            'total_presencas': total_presencas,
            'percentual_frequencia': (total_presencas / max(total_dias, 1)) * 100,
            'media_treinos_semana': (total_presencas / max(total_dias / 7, 1)),
        }
        
        # Evolução de peso
        if dados['medidas']:
            peso_inicial = dados['medidas'][0].peso
            peso_final = dados['medidas'][-1].peso
            dados['estatisticas']['peso_inicial'] = peso_inicial
            dados['estatisticas']['peso_final'] = peso_final
            dados['estatisticas']['diferenca_peso'] = peso_final - peso_inicial
            
            # IMC
            altura = aluno.altura or Decimal('1.70')  # Altura padrão se não informada
            dados['estatisticas']['imc_inicial'] = peso_inicial / (altura ** 2)
            dados['estatisticas']['imc_final'] = peso_final / (altura ** 2)
        
        return dados
    
    def _gerar_graficos(self, relatorio, dados):
        """Gera gráficos para o relatório."""
        graficos = {}
        
        # Configurar estilo dos gráficos
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Gráfico de evolução de peso
        if len(dados['medidas']) > 1:
            graficos['peso'] = self._criar_grafico_peso(dados['medidas'])
        
        # Gráfico de frequência semanal
        if dados['presencas']:
            graficos['frequencia'] = self._criar_grafico_frequencia(dados['presencas'], relatorio.data_inicio, relatorio.data_fim)
        
        # Gráfico de medidas corporais
        if len(dados['medidas']) > 1:
            graficos['medidas'] = self._criar_grafico_medidas(dados['medidas'])
        
        return graficos
    
    def _criar_grafico_peso(self, medidas):
        """Cria gráfico de evolução de peso."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        datas = [m.data_medicao for m in medidas]
        pesos = [float(m.peso) for m in medidas]
        
        ax.plot(datas, pesos, marker='o', linewidth=2, markersize=6, color='#2563eb')
        ax.set_title('Evolução do Peso', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Data', fontsize=12)
        ax.set_ylabel('Peso (kg)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Formatação do eixo X
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(datas)//10)))
        plt.xticks(rotation=45)
        
        # Adicionar anotações nos pontos extremos
        if len(pesos) > 1:
            # Primeiro ponto
            ax.annotate(f'{pesos[0]:.1f} kg', 
                       (datas[0], pesos[0]), 
                       textcoords="offset points", 
                       xytext=(0,10), 
                       ha='center',
                       fontweight='bold')
            
            # Último ponto
            ax.annotate(f'{pesos[-1]:.1f} kg', 
                       (datas[-1], pesos[-1]), 
                       textcoords="offset points", 
                       xytext=(0,10), 
                       ha='center',
                       fontweight='bold')
        
        plt.tight_layout()
        
        # Salvar como base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        grafico_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return grafico_base64
    
    def _criar_grafico_frequencia(self, presencas, data_inicio, data_fim):
        """Cria gráfico de frequência semanal."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Organizar dados por semana
        df_presencas = pd.DataFrame([{'data': p.data_aula} for p in presencas])
        if not df_presencas.empty:
            df_presencas['data'] = pd.to_datetime(df_presencas['data'])
            df_presencas['semana'] = df_presencas['data'].dt.to_period('W')
            
            frequencia_semanal = df_presencas.groupby('semana').size()
            
            semanas = [str(s) for s in frequencia_semanal.index]
            treinos = frequencia_semanal.values
            
            bars = ax.bar(semanas, treinos, color='#059669', alpha=0.8)
            
            # Adicionar valores nas barras
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{int(height)}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom',
                           fontweight='bold')
        
        ax.set_title('Frequência Semanal de Treinos', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Semana', fontsize=12)
        ax.set_ylabel('Número de Treinos', fontsize=12)
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
    
    def _criar_grafico_medidas(self, medidas):
        """Cria gráfico de evolução das medidas corporais."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        datas = [m.data_medicao for m in medidas]
        
        # Braço
        if all(m.braco_direito for m in medidas):
            bracos = [float(m.braco_direito) for m in medidas]
            ax1.plot(datas, bracos, marker='o', color='#dc2626')
            ax1.set_title('Braço (cm)')
            ax1.grid(True, alpha=0.3)
        
        # Peito/Tórax
        if all(m.torax for m in medidas):
            peitorais = [float(m.torax) for m in medidas]
            ax2.plot(datas, peitorais, marker='o', color='#2563eb')
            ax2.set_title('Tórax (cm)')
            ax2.grid(True, alpha=0.3)
        
        # Cintura
        if all(m.cintura for m in medidas):
            cinturas = [float(m.cintura) for m in medidas]
            ax3.plot(datas, cinturas, marker='o', color='#059669')
            ax3.set_title('Cintura (cm)')
            ax3.grid(True, alpha=0.3)
        
        # Coxa
        if all(m.coxa_direita for m in medidas):
            coxas = [float(m.coxa_direita) for m in medidas]
            ax4.plot(datas, coxas, marker='o', color='#7c2d12')
            ax4.set_title('Coxa (cm)')
            ax4.grid(True, alpha=0.3)
        
        plt.suptitle('Evolução das Medidas Corporais', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Salvar como base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        grafico_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return grafico_base64
    
    def _criar_pdf(self, relatorio, dados, graficos):
        """Cria o arquivo PDF do relatório."""
        # Definir caminho do arquivo
        filename = f"relatorio_{relatorio.aluno.id}_{relatorio.data_inicio}_{relatorio.data_fim}.pdf"
        filepath = os.path.join(settings.MEDIA_ROOT, 'relatorios', filename)
        
        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Criar PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Cabeçalho
        story.append(Paragraph(relatorio.titulo, self.titulo_style))
        story.append(Paragraph(f"Aluno: {dados['aluno'].nome}", self.subtitulo_style))
        story.append(Paragraph(f"Período: {dados['periodo']}", self.texto_style))
        story.append(Paragraph(f"Data de geração: {timezone.now().strftime('%d/%m/%Y às %H:%M')}", self.texto_style))
        story.append(Spacer(1, 20))
        
        # Resumo executivo
        story.append(Paragraph("Resumo Executivo", self.subtitulo_style))
        
        if 'peso_inicial' in dados['estatisticas']:
            peso_inicial = dados['estatisticas']['peso_inicial']
            peso_final = dados['estatisticas']['peso_final']
            diferenca = dados['estatisticas']['diferenca_peso']
            
            story.append(Paragraph(f"• Peso inicial: {peso_inicial:.1f} kg", self.texto_style))
            story.append(Paragraph(f"• Peso final: {peso_final:.1f} kg", self.texto_style))
            
            if diferenca > 0:
                story.append(Paragraph(f"• Ganho de peso: +{diferenca:.1f} kg", self.destaque_style))
            elif diferenca < 0:
                story.append(Paragraph(f"• Perda de peso: {diferenca:.1f} kg", self.destaque_style))
            else:
                story.append(Paragraph("• Peso mantido", self.destaque_style))
        
        story.append(Paragraph(f"• Total de treinos: {dados['estatisticas']['total_presencas']}", self.texto_style))
        story.append(Paragraph(f"• Frequência: {dados['estatisticas']['percentual_frequencia']:.1f}%", self.texto_style))
        story.append(Paragraph(f"• Média de treinos por semana: {dados['estatisticas']['media_treinos_semana']:.1f}", self.texto_style))
        
        story.append(Spacer(1, 20))
        
        # Gráficos
        if graficos:
            story.append(Paragraph("Gráficos de Evolução", self.subtitulo_style))
            
            for nome_grafico, grafico_base64 in graficos.items():
                # Decodificar imagem
                grafico_data = base64.b64decode(grafico_base64)
                grafico_buffer = BytesIO(grafico_data)
                
                # Adicionar imagem ao PDF
                img = Image(grafico_buffer, width=15*cm, height=9*cm)
                story.append(img)
                story.append(Spacer(1, 15))
        
        # Observações
        if relatorio.observacoes:
            story.append(Paragraph("Observações", self.subtitulo_style))
            story.append(Paragraph(relatorio.observacoes, self.texto_style))
        
        # Rodapé
        story.append(Spacer(1, 30))
        story.append(Paragraph("FormaFit - Sistema de Gestão para Personal Trainers", self.styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        return f"relatorios/{filename}"
    
    def _calcular_estatisticas(self, relatorio, dados):
        """Atualiza as estatísticas do relatório."""
        stats = dados['estatisticas']
        
        relatorio.total_treinos = stats['total_presencas']
        relatorio.percentual_frequencia = Decimal(str(stats['percentual_frequencia']))
        
        if 'peso_inicial' in stats:
            relatorio.peso_inicial = stats['peso_inicial']
            relatorio.peso_final = stats['peso_final']
            relatorio.diferenca_peso = stats['diferenca_peso']
            relatorio.imc_inicial = Decimal(str(stats['imc_inicial']))
            relatorio.imc_final = Decimal(str(stats['imc_final']))
