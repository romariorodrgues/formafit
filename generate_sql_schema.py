#!/usr/bin/env python
"""
Script para gerar a estrutura SQL completa do banco de dados FormaFit
sem precisar conectar ao PostgreSQL.
"""

import os
import sys
import django
from io import StringIO
from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.apps import apps

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')

# Usar SQLite temporariamente para gerar o SQL
os.environ['USE_SQLITE'] = 'True'

django.setup()

def generate_sql_schema():
    """Gera a estrutura SQL completa do banco de dados"""
    
    print("=" * 60)
    print("FORMAFIT - GERADOR DE ESTRUTURA SQL POSTGRESQL")
    print("=" * 60)
    print()
    
    # Capturar a saída do comando sqlmigrate
    sql_output = StringIO()
    
    # Lista de apps na ordem correta de dependências
    apps_order = [
        'contenttypes',
        'auth', 
        'admin',
        'sessions',
        'messages',
        'staticfiles',
        'accounts',
        'alunos', 
        'treinos',
        'frequencia',
        'financeiro',
        'relatorios',
        'notificacoes'
    ]
    
    sql_statements = []
    
    print("Gerando SQL para cada app...")
    
    # Adicionar header do arquivo SQL
    sql_statements.append("""-- =====================================================
-- FORMAFIT - ESTRUTURA COMPLETA DO BANCO DE DADOS
-- Sistema para Personal Trainers
-- =====================================================
-- 
-- Este arquivo contém a estrutura completa das tabelas
-- do sistema FormaFit para PostgreSQL.
--
-- Para usar:
-- 1. Crie o banco: CREATE DATABASE formafit_db;
-- 2. Crie o usuário: CREATE USER formafit_user WITH PASSWORD 'formafit123';
-- 3. Execute: psql -d formafit_db -f database_schema.sql
--
-- =====================================================

-- Configurações iniciais
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;

-- =====================================================
-- INÍCIO DAS TABELAS
-- =====================================================

""")
    
    try:
        # Para cada app, pegar todas as migrações
        for app_name in apps_order:
            try:
                app_config = apps.get_app_config(app_name)
                migrations_dir = os.path.join(app_config.path, 'migrations')
                
                if os.path.exists(migrations_dir):
                    print(f"  - Processando {app_name}...")
                    
                    # Listar arquivos de migração
                    migration_files = [
                        f for f in os.listdir(migrations_dir) 
                        if f.endswith('.py') and f != '__init__.py' and not f.startswith('.')
                    ]
                    migration_files.sort()
                    
                    sql_statements.append(f"\n-- =====================================================")
                    sql_statements.append(f"-- {app_name.upper()} APP")
                    sql_statements.append(f"-- =====================================================\n")
                    
                    for migration_file in migration_files:
                        migration_name = migration_file[:-3]  # Remove .py
                        
                        try:
                            # Capturar SQL da migração
                            output = StringIO()
                            call_command('sqlmigrate', app_name, migration_name, stdout=output)
                            sql_content = output.getvalue()
                            
                            if sql_content.strip():
                                sql_statements.append(f"-- Migração: {app_name}.{migration_name}")
                                sql_statements.append(sql_content)
                                sql_statements.append("")
                                
                        except Exception as e:
                            print(f"    Aviso: Não foi possível processar {migration_name}: {e}")
                            
            except Exception as e:
                print(f"  Aviso: App {app_name} não encontrado ou erro: {e}")
                continue
    
    except Exception as e:
        print(f"Erro ao processar migrações: {e}")
    
    # Adicionar comandos finais
    sql_statements.append("""
-- =====================================================
-- CONFIGURAÇÕES FINAIS
-- =====================================================

-- Conceder permissões ao usuário
GRANT ALL PRIVILEGES ON DATABASE formafit_db TO formafit_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO formafit_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO formafit_user;

-- Permitir que o usuário crie tabelas
ALTER USER formafit_user CREATEDB;

-- =====================================================
-- FIM DO ARQUIVO
-- =====================================================
""")
    
    # Escrever arquivo SQL
    sql_file_path = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
    
    with open(sql_file_path, 'w', encoding='utf-8') as f:
        for statement in sql_statements:
            f.write(statement)
    
    print(f"\n✅ Arquivo SQL gerado com sucesso: {sql_file_path}")
    print(f"📝 Total de comandos SQL: {len(sql_statements)}")
    
    return sql_file_path

if __name__ == "__main__":
    generate_sql_schema()
