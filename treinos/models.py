"""
Modelos para gerenciamento de treinos e exercícios.
"""
from django.db import models
from django.utils import timezone
from alunos.models import Aluno


class Exercicio(models.Model):
    """
    Catálogo de exercícios disponíveis.
    """
    GRUPO_MUSCULAR_CHOICES = [
        ('peito', 'Peito'),
        ('costas', 'Costas'),
        ('ombros', 'Ombros'),
        ('biceps', 'Bíceps'),
        ('triceps', 'Tríceps'),
        ('quadriceps', 'Quadríceps'),
        ('posterior', 'Posterior de Coxa'),
        ('gluteos', 'Glúteos'),
        ('panturrilha', 'Panturrilha'),
        ('abdomen', 'Abdômen'),
        ('cardio', 'Cardio'),
        ('funcional', 'Funcional'),
    ]
    
    CATEGORIA_CHOICES = [
        ('forca', 'Força'),
        ('cardio', 'Cardio'),
        ('flexibilidade', 'Flexibilidade'),
        ('funcional', 'Funcional'),
    ]
    
    EQUIPAMENTO_CHOICES = [
        ('livre', 'Peso Livre'),
        ('maquina', 'Máquina'),
        ('cabo', 'Cabo/Polia'),
        ('corporal', 'Peso Corporal'),
        ('funcional', 'Funcional'),
        ('cardio', 'Cardio'),
        ('outro', 'Outro'),
    ]
    
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    grupo_muscular = models.CharField(max_length=20, choices=GRUPO_MUSCULAR_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    equipamento = models.CharField(max_length=20, choices=EQUIPAMENTO_CHOICES, default='livre')
    instrucoes = models.TextField(blank=True, help_text="Instruções de execução")
    video_url = models.URLField(blank=True, help_text="Link para vídeo demonstrativo")
    imagem = models.ImageField(upload_to='exercicios/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Exercício'
        verbose_name_plural = 'Exercícios'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class PlanoTreino(models.Model):
    """
    Plano de treino para um aluno específico.
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='planos_treino')
    nome = models.CharField(max_length=200, help_text="Nome do plano de treino")
    descricao = models.TextField(blank=True)
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(blank=True, null=True)
    duracao_semanas = models.IntegerField(default=4, help_text="Duração em semanas")
    ativo = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    personal_trainer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='planos_criados', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Plano de Treino'
        verbose_name_plural = 'Planos de Treino'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.nome}"


class TreinoDiario(models.Model):
    """
    Treino específico para um dia da semana.
    """
    DIAS_SEMANA = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    
    plano_treino = models.ForeignKey(PlanoTreino, on_delete=models.CASCADE, related_name='dias_treino')
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA)
    nome = models.CharField(max_length=200, help_text="Ex: Treino A - Peito e Tríceps")
    descricao = models.TextField(blank=True)
    tempo_estimado = models.IntegerField(help_text="Tempo estimado em minutos", blank=True, null=True)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Treino Diário'
        verbose_name_plural = 'Treinos Diários'
        ordering = ['dia_semana']
        unique_together = ['plano_treino', 'dia_semana']
    
    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.nome}"


class ExercicioTreino(models.Model):
    """
    Exercício específico dentro de um treino diário.
    """
    treino_diario = models.ForeignKey(TreinoDiario, on_delete=models.CASCADE, related_name='exercicios')
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    ordem = models.IntegerField(help_text="Ordem de execução no treino")
    
    # Especificações do exercício
    series = models.IntegerField(help_text="Número de séries")
    repeticoes = models.CharField(max_length=50, help_text="Ex: 12-15, até a falha, 30 seg")
    carga = models.CharField(max_length=50, blank=True, help_text="Ex: 20kg, corpo livre")
    tempo_descanso = models.CharField(max_length=50, blank=True, help_text="Tempo de descanso entre séries")
    observacoes = models.TextField(blank=True, help_text="Observações específicas")
    
    class Meta:
        verbose_name = 'Exercício do Treino'
        verbose_name_plural = 'Exercícios do Treino'
        ordering = ['ordem']
        unique_together = ['treino_diario', 'ordem']
    
    def __str__(self):
        return f"{self.treino_diario.nome} - {self.exercicio.nome}"


class RegistroTreino(models.Model):
    """
    Registro de execução de um treino pelo aluno.
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='registros_treino')
    treino_diario = models.ForeignKey(TreinoDiario, on_delete=models.CASCADE, related_name='registros')
    data_execucao = models.DateTimeField(default=timezone.now)
    tempo_total = models.IntegerField(help_text="Tempo total em minutos", blank=True, null=True)
    observacoes = models.TextField(blank=True, help_text="Observações sobre a execução do treino")
    avaliacoes = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True, help_text="Avaliação de 1 a 5")
    
    class Meta:
        verbose_name = 'Registro de Treino'
        verbose_name_plural = 'Registros de Treino'
        ordering = ['-data_execucao']
    
    def __str__(self):
        return f"{self.aluno.nome} - {self.treino_diario.nome} - {self.data_execucao.strftime('%d/%m/%Y')}"


class RegistroExercicio(models.Model):
    """
    Registro específico de cada exercício executado.
    """
    registro_treino = models.ForeignKey(RegistroTreino, on_delete=models.CASCADE, related_name='exercicios_executados')
    exercicio_treino = models.ForeignKey(ExercicioTreino, on_delete=models.CASCADE)
    series_executadas = models.IntegerField()
    repeticoes_executadas = models.CharField(max_length=200, help_text="Repetições por série, separadas por vírgula")
    carga_utilizada = models.CharField(max_length=50, blank=True)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Registro de Exercício'
        verbose_name_plural = 'Registros de Exercícios'
    
    def __str__(self):
        return f"{self.exercicio_treino.exercicio.nome} - {self.series_executadas} séries"
