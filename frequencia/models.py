"""
Modelos para controle de frequência dos alunos.
"""
from django.db import models
from django.utils import timezone
from alunos.models import Aluno


class RegistroPresenca(models.Model):
    """
    Registro de presença dos alunos nas aulas.
    """
    STATUS_CHOICES = [
        ('presente', 'Presente'),
        ('falta', 'Falta'),
        ('falta_justificada', 'Falta Justificada'),
        ('cancelado', 'Cancelado'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='registros_presenca')
    data_aula = models.DateField(default=timezone.now)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    observacoes = models.TextField(blank=True, help_text="Observações sobre a aula ou falta")
    data_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Registro de Presença'
        verbose_name_plural = 'Registros de Presença'
        ordering = ['-data_aula', 'horario_inicio']
        unique_together = ['aluno', 'data_aula', 'horario_inicio']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.data_aula.strftime('%d/%m/%Y')} - {self.get_status_display()}"
    
    @property
    def duracao_aula(self):
        """Calcula a duração da aula em minutos."""
        if self.horario_inicio and self.horario_fim:
            inicio = timezone.datetime.combine(timezone.now().date(), self.horario_inicio)
            fim = timezone.datetime.combine(timezone.now().date(), self.horario_fim)
            duracao = fim - inicio
            return duracao.total_seconds() / 60
        return None


class AgendaAula(models.Model):
    """
    Agendamento de aulas futuras.
    """
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('confirmado', 'Confirmado'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
        ('remarcado', 'Remarcado'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='aulas_agendadas')
    data_aula = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='agendado')
    tipo_treino = models.CharField(max_length=200, blank=True, help_text="Ex: Treino A, Avaliação, etc.")
    observacoes = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Agendamento de Aula'
        verbose_name_plural = 'Agendamentos de Aulas'
        ordering = ['data_aula', 'horario_inicio']
        unique_together = ['aluno', 'data_aula', 'horario_inicio']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.data_aula.strftime('%d/%m/%Y')} às {self.horario_inicio.strftime('%H:%M')}"
    
    def save(self, *args, **kwargs):
        """
        Ao marcar como realizado, criar automaticamente um registro de presença.
        """
        if self.status == 'realizado':
            # Verificar se já existe um registro de presença
            if not RegistroPresenca.objects.filter(
                aluno=self.aluno,
                data_aula=self.data_aula,
                horario_inicio=self.horario_inicio
            ).exists():
                RegistroPresenca.objects.create(
                    aluno=self.aluno,
                    data_aula=self.data_aula,
                    horario_inicio=self.horario_inicio,
                    horario_fim=self.horario_fim,
                    status='presente',
                    observacoes=f"Aula realizada - {self.tipo_treino}"
                )
        
        super().save(*args, **kwargs)


class RelatorioFrequencia(models.Model):
    """
    Relatório de frequência mensal dos alunos.
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='relatorios_frequencia')
    mes = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    ano = models.IntegerField()
    total_aulas_agendadas = models.IntegerField(default=0)
    total_presencas = models.IntegerField(default=0)
    total_faltas = models.IntegerField(default=0)
    total_faltas_justificadas = models.IntegerField(default=0)
    percentual_frequencia = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    data_geracao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Relatório de Frequência'
        verbose_name_plural = 'Relatórios de Frequência'
        ordering = ['-ano', '-mes']
        unique_together = ['aluno', 'mes', 'ano']
    
    def __str__(self):
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        return f"{self.aluno.nome} - {meses[self.mes]}/{self.ano} - {self.percentual_frequencia}%"
    
    @classmethod
    def gerar_relatorio_mensal(cls, aluno, mes, ano):
        """
        Gera ou atualiza o relatório de frequência mensal.
        """
        registros = RegistroPresenca.objects.filter(
            aluno=aluno,
            data_aula__month=mes,
            data_aula__year=ano
        )
        
        total_aulas = registros.count()
        presencas = registros.filter(status='presente').count()
        faltas = registros.filter(status='falta').count()
        faltas_justificadas = registros.filter(status='falta_justificada').count()
        
        if total_aulas > 0:
            percentual = (presencas / total_aulas) * 100
        else:
            percentual = 0
        
        relatorio, created = cls.objects.update_or_create(
            aluno=aluno,
            mes=mes,
            ano=ano,
            defaults={
                'total_aulas_agendadas': total_aulas,
                'total_presencas': presencas,
                'total_faltas': faltas,
                'total_faltas_justificadas': faltas_justificadas,
                'percentual_frequencia': round(percentual, 2)
            }
        )
        
        return relatorio
