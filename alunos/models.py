"""
Modelos para gerenciamento de alunos.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Aluno(models.Model):
    """
    Modelo para representar um aluno do personal trainer.
    """
    OBJETIVO_CHOICES = [
        ('saude_geral', 'Melhorar saúde geral'),
        ('emagrecimento', 'Emagrecimento'),
        ('hipertrofia', 'Hipertrofia'),
    ]
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]
    
    DIAS_SEMANA_CHOICES = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    # Dados pessoais
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    endereco = models.TextField(blank=True)
    
    # Dados físicos iniciais
    peso_inicial = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso em kg")
    altura = models.DecimalField(max_digits=4, decimal_places=2, help_text="Altura em metros")
    
    # Objetivos e observações
    objetivo = models.CharField(max_length=20, choices=OBJETIVO_CHOICES)
    observacoes = models.TextField(blank=True, help_text="Observações gerais, histórico médico, etc.")
    
    # Agendamento padrão
    dia_semana_treino = models.IntegerField(choices=DIAS_SEMANA_CHOICES, blank=True, null=True, help_text="Dia da semana fixo para treino")
    horario_treino = models.TimeField(blank=True, null=True, help_text="Horário fixo para treino")
    
    # Relacionamento com personal trainer
    personal_trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alunos')
    
    # Dados de controle
    ativo = models.BooleanField(default=True)
    data_inicio = models.DateField(default=timezone.now)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def idade(self):
        """Calcula a idade do aluno."""
        hoje = timezone.now().date()
        idade = hoje.year - self.data_nascimento.year
        if hoje.month < self.data_nascimento.month or (hoje.month == self.data_nascimento.month and hoje.day < self.data_nascimento.day):
            idade -= 1
        return idade
    
    @property
    def imc_inicial(self):
        """Calcula o IMC inicial do aluno."""
        if self.peso_inicial and self.altura:
            return float(self.peso_inicial) / (float(self.altura) ** 2)
        return None
    
    def get_proximo_treino(self):
        """Retorna a próxima data de treino baseada no agendamento padrão."""
        if self.dia_semana_treino is not None and self.horario_treino:
            from datetime import datetime, timedelta
            hoje = timezone.now().date()
            dias_ate_treino = (self.dia_semana_treino - hoje.weekday()) % 7
            if dias_ate_treino == 0:
                # Se é hoje, verifica se o horário já passou
                agora = timezone.now().time()
                if agora > self.horario_treino:
                    dias_ate_treino = 7
            proxima_data = hoje + timedelta(days=dias_ate_treino)
            return proxima_data
        return None
    
    def criar_agendamentos_automaticos(self, semanas=4):
        """Cria agendamentos automáticos para as próximas semanas."""
        if self.dia_semana_treino is not None and self.horario_treino:
            from datetime import timedelta
            from frequencia.models import AgendaAula
            
            proxima_data = self.get_proximo_treino()
            if proxima_data:
                agendamentos_criados = []
                for i in range(semanas):
                    data_treino = proxima_data + timedelta(weeks=i)
                    
                    # Verifica se já existe agendamento para esta data
                    if not AgendaAula.objects.filter(
                        aluno=self,
                        data_aula=data_treino,
                        horario_inicio=self.horario_treino
                    ).exists():
                        # Calcula horário de fim (1 hora de duração padrão)
                        from datetime import datetime, timedelta
                        horario_inicio = self.horario_treino
                        if isinstance(horario_inicio, str):
                            from datetime import time
                            hora, minuto = map(int, horario_inicio.split(':'))
                            horario_inicio = time(hora, minuto)
                        
                        horario_fim = (
                            datetime.combine(data_treino, horario_inicio) + 
                            timedelta(hours=1)
                        ).time()
                        
                        agendamento = AgendaAula.objects.create(
                            aluno=self,
                            data_aula=data_treino,
                            horario_inicio=horario_inicio,
                            horario_fim=horario_fim,
                            status='agendado',
                            tipo_treino='Treino Regular'
                        )
                        agendamentos_criados.append(agendamento)
                
                return agendamentos_criados
        return []


class MedidasCorporais(models.Model):
    """
    Modelo para armazenar medidas corporais do aluno ao longo do tempo.
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='medidas')
    data_medicao = models.DateField(default=timezone.now)
    
    # Medidas básicas
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso em kg")
    percentual_gordura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    
    # Medidas específicas (em cm)
    pescoco = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    torax = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    cintura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    quadril = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    braco_direito = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    braco_esquerdo = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    coxa_direita = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    coxa_esquerda = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    
    # Observações
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Medidas Corporais'
        verbose_name_plural = 'Medidas Corporais'
        ordering = ['-data_medicao']
        unique_together = ['aluno', 'data_medicao']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.data_medicao.strftime('%d/%m/%Y')}"
    
    @property
    def imc(self):
        """Calcula o IMC para esta medição."""
        if self.peso and self.aluno.altura:
            return float(self.peso) / (float(self.aluno.altura) ** 2)
        return None


class FotoProgresso(models.Model):
    """
    Modelo para armazenar fotos de progresso do aluno.
    """
    TIPO_FOTO_CHOICES = [
        ('frente', 'Frente'),
        ('lado', 'Lado'),
        ('costas', 'Costas'),
        ('outro', 'Outro'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='fotos_progresso')
    data_foto = models.DateField(default=timezone.now)
    tipo_foto = models.CharField(max_length=10, choices=TIPO_FOTO_CHOICES)
    foto = models.ImageField(upload_to='progresso/')
    descricao = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'Foto de Progresso'
        verbose_name_plural = 'Fotos de Progresso'
        ordering = ['-data_foto']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.tipo_foto} - {self.data_foto.strftime('%d/%m/%Y')}"
