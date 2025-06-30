"""
Modelos para geração e gerenciamento de relatórios.
"""
from django.db import models
from django.utils import timezone
from django.conf import settings
from alunos.models import Aluno
import uuid


class TipoRelatorio(models.Model):
    """
    Tipos de relatórios disponíveis no sistema.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    template_filename = models.CharField(max_length=200, help_text="Nome do template HTML")
    ativo = models.BooleanField(default=True)
    
    # Configurações de geração
    incluir_graficos = models.BooleanField(default=True)
    incluir_fotos = models.BooleanField(default=True)
    incluir_medidas = models.BooleanField(default=True)
    incluir_frequencia = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tipo de Relatório'
        verbose_name_plural = 'Tipos de Relatório'
    
    def __str__(self):
        return self.nome


class RelatorioProgresso(models.Model):
    """
    Relatórios de progresso dos alunos.
    """
    STATUS_CHOICES = [
        ('gerando', 'Gerando'),
        ('concluido', 'Concluído'),
        ('erro', 'Erro na Geração'),
        ('enviado', 'Enviado'),
    ]
    
    PERIODO_CHOICES = [
        ('semanal', 'Semanal'),
        ('mensal', 'Mensal'),
        ('trimestral', 'Trimestral'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
        ('personalizado', 'Período Personalizado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='relatorios_progresso')
    tipo_relatorio = models.ForeignKey(TipoRelatorio, on_delete=models.CASCADE)
    personal_trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='relatorios_gerados')
    
    titulo = models.CharField(max_length=200)
    periodo = models.CharField(max_length=15, choices=PERIODO_CHOICES)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='gerando')
    arquivo_pdf = models.FileField(upload_to='relatorios/', blank=True, null=True)
    
    # Dados do relatório
    peso_inicial = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    peso_final = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    diferenca_peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    imc_inicial = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    imc_final = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    total_treinos = models.IntegerField(default=0)
    percentual_frequencia = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    observacoes = models.TextField(blank=True)
    data_geracao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Relatório de Progresso'
        verbose_name_plural = 'Relatórios de Progresso'
        ordering = ['-data_geracao']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.titulo} - {self.data_inicio.strftime('%d/%m/%Y')}"
    
    @property
    def url_download(self):
        """URL para download do relatório."""
        if self.arquivo_pdf:
            return self.arquivo_pdf.url
        return None
    
    def calcular_estatisticas(self):
        """Calcula as estatísticas do relatório."""
        from alunos.models import MedidasCorporais
        from frequencia.models import RegistroPresenca
        from treinos.models import RegistroTreino
        
        # Buscar medidas no período
        medidas = MedidasCorporais.objects.filter(
            aluno=self.aluno,
            data_medicao__range=[self.data_inicio, self.data_fim]
        ).order_by('data_medicao')
        
        if medidas.exists():
            primeira_medida = medidas.first()
            ultima_medida = medidas.last()
            
            self.peso_inicial = primeira_medida.peso
            self.peso_final = ultima_medida.peso
            self.diferenca_peso = self.peso_final - self.peso_inicial
            
            self.imc_inicial = primeira_medida.imc
            self.imc_final = ultima_medida.imc
        
        # Calcular frequência
        presencas = RegistroPresenca.objects.filter(
            aluno=self.aluno,
            data_aula__range=[self.data_inicio, self.data_fim]
        )
        total_aulas = presencas.count()
        presencas_efetivas = presencas.filter(status='presente').count()
        
        if total_aulas > 0:
            self.percentual_frequencia = (presencas_efetivas / total_aulas) * 100
        
        # Contar treinos realizados
        self.total_treinos = RegistroTreino.objects.filter(
            aluno=self.aluno,
            data_execucao__date__range=[self.data_inicio, self.data_fim]
        ).count()
        
        self.save()


class DadosRelatorio(models.Model):
    """
    Dados específicos incluídos no relatório.
    """
    relatorio = models.ForeignKey(RelatorioProgresso, on_delete=models.CASCADE, related_name='dados')
    data = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    percentual_gordura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    medidas_json = models.JSONField(blank=True, null=True, help_text="Medidas corporais em formato JSON")
    treinos_realizados = models.IntegerField(default=0)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Dados do Relatório'
        verbose_name_plural = 'Dados dos Relatórios'
        ordering = ['data']
        unique_together = ['relatorio', 'data']
    
    def __str__(self):
        return f"{self.relatorio.titulo} - {self.data.strftime('%d/%m/%Y')}"


class TemplateRelatorio(models.Model):
    """
    Templates HTML para geração de relatórios.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    conteudo_html = models.TextField(help_text="Código HTML do template")
    css_personalizado = models.TextField(blank=True, help_text="CSS personalizado para o template")
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Template de Relatório'
        verbose_name_plural = 'Templates de Relatório'
    
    def __str__(self):
        return self.nome


class CompartilhamentoRelatorio(models.Model):
    """
    Controle de compartilhamento de relatórios.
    """
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('expirado', 'Expirado'),
        ('revogado', 'Revogado'),
    ]
    
    relatorio = models.ForeignKey(RelatorioProgresso, on_delete=models.CASCADE, related_name='compartilhamentos')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    email_compartilhado = models.EmailField(blank=True)
    data_expiracao = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')
    acessos = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultimo_acesso = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Compartilhamento de Relatório'
        verbose_name_plural = 'Compartilhamentos de Relatórios'
    
    def __str__(self):
        return f"Compartilhamento - {self.relatorio.titulo}"
    
    @property
    def esta_valido(self):
        """Verifica se o compartilhamento ainda é válido."""
        return (self.status == 'ativo' and 
                timezone.now() < self.data_expiracao)
    
    def registrar_acesso(self):
        """Registra um novo acesso ao relatório."""
        if self.esta_valido:
            self.acessos += 1
            self.ultimo_acesso = timezone.now()
            self.save()
            return True
        return False


class EstatisticaRelatorio(models.Model):
    """
    Estatísticas de uso dos relatórios.
    """
    personal_trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='estatisticas_relatorios')
    mes = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    ano = models.IntegerField()
    
    total_relatorios_gerados = models.IntegerField(default=0)
    total_relatorios_enviados = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)
    total_compartilhamentos = models.IntegerField(default=0)
    
    relatorio_mais_gerado = models.CharField(max_length=200, blank=True)
    periodo_mais_usado = models.CharField(max_length=15, blank=True)
    
    data_geracao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Estatística de Relatório'
        verbose_name_plural = 'Estatísticas de Relatórios'
        unique_together = ['personal_trainer', 'mes', 'ano']
        ordering = ['-ano', '-mes']
    
    def __str__(self):
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"Estatísticas {self.personal_trainer.nome_completo} - {meses[self.mes]}/{self.ano}"
