#!/usr/bin/env python
"""
Script para criar um superusuário para teste.
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def criar_superusuario():
    """
    Cria um superusuário para teste.
    """
    try:
        # Verificar se já existe um superusuário
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superusuário já existe")
            superuser = User.objects.filter(is_superuser=True).first()
            print(f"   Username: {superuser.username}")
            print(f"   Email: {superuser.email}")
            return
        
        # Criar superusuário
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@formafit.com',
            password='admin123'
        )
        print("✅ Superusuário criado com sucesso!")
        print(f"   Username: {superuser.username}")
        print(f"   Email: {superuser.email}")
        print(f"   Password: admin123")
        
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    criar_superusuario()
