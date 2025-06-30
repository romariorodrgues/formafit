"""
Modelos para gestão financeira dos alunos.
"""
from django.db import models
from django.utils import timezone
from decimal import Decimal
from alunos.models import Aluno


class PlanoMensalidade(models.Model):
    """
    Planos de mensalidade disponíveis.
    """
    nome = models.CharField(max_length=200, help_text="Ex: Plano Básico, Plano Premium")
    descricao = models.TextField(blank=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    aulas_incluidas = models.IntegerField(help_text="Número de aulas incluídas no plano")
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Plano de Mensalidade'
        verbose_name_plural = 'Planos de Mensalidade'
        ordering = ['valor']
    
    def __str__(self):
        return f"{self.nome} - R$ {self.valor}"


class ContratoAluno(models.Model):
    """
    Contrato financeiro do aluno com o personal trainer.
    """
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, related_name='contrato')
    plano_mensalidade = models.ForeignKey(PlanoMensalidade, on_delete=models.PROTECT)
    valor_personalizado = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, 
                                            help_text="Valor personalizado, se diferente do plano")
    dia_vencimento = models.IntegerField(default=5, help_text="Dia do mês para vencimento")
    ativo = models.BooleanField(default=True)
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(blank=True, null=True)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Contrato do Aluno'
        verbose_name_plural = 'Contratos dos Alunos'
    
    def __str__(self):
        return f"Contrato - {self.aluno.nome}"
    
    @property
    def valor_mensalidade(self):
        """Retorna o valor da mensalidade (personalizado ou do plano)."""
        return self.valor_personalizado or self.plano_mensalidade.valor


class Fatura(models.Model):
    """
    Faturas mensais dos alunos.
    """
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('paga', 'Paga'),
        ('atrasada', 'Atrasada'),
        ('cancelada', 'Cancelada'),
        ('parcial', 'Paga Parcialmente'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='faturas')
    contrato = models.ForeignKey(ContratoAluno, on_delete=models.CASCADE, related_name='faturas')
    mes_referencia = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    ano_referencia = models.IntegerField()
    valor_original = models.DecimalField(max_digits=8, decimal_places=2)
    desconto = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    acrescimo = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    valor_final = models.DecimalField(max_digits=8, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'
        ordering = ['-ano_referencia', '-mes_referencia']
        unique_together = ['aluno', 'mes_referencia', 'ano_referencia']
    
    def __str__(self):
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"{self.aluno.nome} - {meses[self.mes_referencia]}/{self.ano_referencia} - R$ {self.valor_final}"
    
    def save(self, *args, **kwargs):
        """Calcula o valor final antes de salvar."""
        self.valor_final = self.valor_original - self.desconto + self.acrescimo
        super().save(*args, **kwargs)
    
    @property
    def esta_atrasada(self):
        """Verifica se a fatura está atrasada."""
        return timezone.now().date() > self.data_vencimento and self.status in ['pendente', 'parcial']
    
    @property
    def dias_atraso(self):
        """Calcula quantos dias a fatura está atrasada."""
        if self.esta_atrasada:
            return (timezone.now().date() - self.data_vencimento).days
        return 0


class Pagamento(models.Model):
    """
    Registros de pagamentos das faturas.
    """
    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('transferencia', 'Transferência Bancária'),
        ('boleto', 'Boleto'),
        ('outro', 'Outro'),
    ]
    
    fatura = models.ForeignKey(Fatura, on_delete=models.CASCADE, related_name='pagamentos')
    data_pagamento = models.DateField(default=timezone.now)
    valor_pago = models.DecimalField(max_digits=8, decimal_places=2)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    observacoes = models.TextField(blank=True)
    comprovante = models.ImageField(upload_to='comprovantes/', blank=True, null=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_pagamento']
    
    def __str__(self):
        return f"Pagamento - {self.fatura.aluno.nome} - R$ {self.valor_pago} - {self.data_pagamento.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        """Atualiza o status da fatura após o pagamento."""
        super().save(*args, **kwargs)
        
        # Recalcular o status da fatura
        total_pago = sum(pagamento.valor_pago for pagamento in self.fatura.pagamentos.all())
        
        if total_pago >= self.fatura.valor_final:
            self.fatura.status = 'paga'
        elif total_pago > 0:
            self.fatura.status = 'parcial'
        else:
            self.fatura.status = 'pendente'
        
        self.fatura.save()


class RelatorioFinanceiro(models.Model):
    """
    Relatórios financeiros mensais.
    """
    mes = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    ano = models.IntegerField()
    total_faturado = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_recebido = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_pendente = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_atrasado = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    numero_alunos_ativos = models.IntegerField(default=0)
    numero_faturas_pagas = models.IntegerField(default=0)
    numero_faturas_pendentes = models.IntegerField(default=0)
    data_geracao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Relatório Financeiro'
        verbose_name_plural = 'Relatórios Financeiros'
        ordering = ['-ano', '-mes']
        unique_together = ['mes', 'ano']
    
    def __str__(self):
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"Relatório Financeiro - {meses[self.mes]}/{self.ano}"
    
    @classmethod
    def gerar_relatorio_mensal(cls, mes, ano):
        """
        Gera ou atualiza o relatório financeiro mensal.
        """
        from django.db.models import Sum, Count
        
        faturas_mes = Fatura.objects.filter(mes_referencia=mes, ano_referencia=ano)
        pagamentos_mes = Pagamento.objects.filter(
            data_pagamento__month=mes,
            data_pagamento__year=ano
        )
        
        total_faturado = faturas_mes.aggregate(total=Sum('valor_final'))['total'] or Decimal('0.00')
        total_recebido = pagamentos_mes.aggregate(total=Sum('valor_pago'))['total'] or Decimal('0.00')
        
        faturas_pendentes = faturas_mes.filter(status__in=['pendente', 'parcial'])
        total_pendente = faturas_pendentes.aggregate(total=Sum('valor_final'))['total'] or Decimal('0.00')
        
        faturas_atrasadas = faturas_mes.filter(
            status__in=['pendente', 'parcial'],
            data_vencimento__lt=timezone.now().date()
        )
        total_atrasado = faturas_atrasadas.aggregate(total=Sum('valor_final'))['total'] or Decimal('0.00')
        
        # Contar alunos ativos no mês
        alunos_ativos = Aluno.objects.filter(
            ativo=True,
            data_inicio__lte=timezone.date(ano, mes, 1)
        ).count()
        
        relatorio, created = cls.objects.update_or_create(
            mes=mes,
            ano=ano,
            defaults={
                'total_faturado': total_faturado,
                'total_recebido': total_recebido,
                'total_pendente': total_pendente,
                'total_atrasado': total_atrasado,
                'numero_alunos_ativos': alunos_ativos,
                'numero_faturas_pagas': faturas_mes.filter(status='paga').count(),
                'numero_faturas_pendentes': faturas_pendentes.count(),
            }
        )
        
        return relatorio
