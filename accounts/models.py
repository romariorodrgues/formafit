"""
Modelos para autenticação e usuários do FormaFit.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modelo customizado de usuário para personal trainers.
    """
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    cref = models.CharField(max_length=20, blank=True, help_text="Número do CREF")
    bio = models.TextField(max_length=500, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Personal Trainer'
        verbose_name_plural = 'Personal Trainers'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def nome_completo(self):
        return f"{self.first_name} {self.last_name}".strip()
