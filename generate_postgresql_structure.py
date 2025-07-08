#!/usr/bin/env python
"""
Script para gerar a estrutura SQL do banco PostgreSQL do FormaFit.
Gera um arquivo SQL com todas as tabelas, índices e constraints.
"""

import os
import sys
import django
from io import StringIO
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')

# Configurar para usar SQLite temporariamente para gerar SQL
os.environ['USE_SQLITE'] = 'True'

django.setup()

from django.core.management import call_command
from django.core.management.commands.sqlmigrate import Command as SqlMigrateCommand
from django.db import connection
from django.apps import apps


def generate_postgresql_schema():
    """Gera o schema PostgreSQL completo."""
    
    print("🚀 Gerando estrutura SQL do PostgreSQL para FormaFit...")
    
    # Arquivo de saída
    output_file = BASE_DIR / 'database_postgresql_schema.sql'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header do arquivo
        f.write("""-- =================================================================
-- FORMAFIT - ESTRUTURA DO BANCO POSTGRESQL
-- =================================================================
-- Sistema completo para personal trainers
-- Gestão de alunos, treinos, frequência e finanças
-- 
-- Data de geração: {date}
-- Versão: 1.0
-- =================================================================

-- Criar usuário e banco se não existirem
-- Execute estes comandos como superuser do PostgreSQL:
/*
CREATE USER formafit_user WITH PASSWORD 'formafit123';
CREATE DATABASE formafit_db OWNER formafit_user;
GRANT ALL PRIVILEGES ON DATABASE formafit_db TO formafit_user;
ALTER USER formafit_user CREATEDB;
*/

-- Conectar ao banco formafit_db antes de executar o restante
\\c formafit_db;

-- Dar permissões ao usuário
GRANT ALL ON SCHEMA public TO formafit_user;

-- =================================================================
-- ESTRUTURA DAS TABELAS
-- =================================================================

""".format(date=str(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))))

        # Obter todas as migrações aplicadas
        apps_with_migrations = [
            'auth',
            'contenttypes', 
            'sessions',
            'admin',
            'accounts',
            'alunos',
            'treinos',
            'frequencia',
            'financeiro',
            'relatorios',
            'notificacoes',
        ]
        
        for app_label in apps_with_migrations:
            try:
                app_config = apps.get_app_config(app_label)
                f.write(f"\n-- =============================================\n")
                f.write(f"-- APP: {app_label.upper()}\n")
                f.write(f"-- =============================================\n\n")
                
                # Obter models do app
                models = app_config.get_models()
                
                for model in models:
                    table_name = model._meta.db_table
                    f.write(f"-- Tabela: {table_name}\n")
                    
                    # Gerar SQL para criação da tabela
                    sql = generate_table_sql(model)
                    f.write(sql)
                    f.write("\n\n")
                    
            except Exception as e:
                print(f"⚠️  Erro ao processar app {app_label}: {e}")
                continue
        
        # Footer
        f.write("""
-- =================================================================
-- ÍNDICES ADICIONAIS E OTIMIZAÇÕES
-- =================================================================

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_alunos_ativo ON alunos_aluno(ativo);
CREATE INDEX IF NOT EXISTS idx_alunos_nome ON alunos_aluno(nome);
CREATE INDEX IF NOT EXISTS idx_financeiro_vencimento ON financeiro_fatura(vencimento);
CREATE INDEX IF NOT EXISTS idx_financeiro_status ON financeiro_fatura(status);
CREATE INDEX IF NOT EXISTS idx_notificacoes_enviado ON notificacoes_notificacao(data_envio);

-- =================================================================
-- DADOS INICIAIS (OPCIONAL)
-- =================================================================

-- Inserir dados básicos se necessário
-- INSERT INTO ... ;

-- =================================================================
-- PERMISSÕES FINAIS
-- =================================================================

-- Garantir que o usuário tenha todas as permissões
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO formafit_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO formafit_user;

-- =================================================================
-- FIM DO SCRIPT
-- =================================================================
""")
    
    print(f"✅ Estrutura SQL gerada: {output_file}")
    print(f"📄 Total de linhas: {count_lines(output_file)}")
    
    return output_file


def generate_table_sql(model):
    """Gera SQL para criação de uma tabela específica."""
    from django.db import connection
    
    table_name = model._meta.db_table
    sql_parts = []
    
    # CREATE TABLE
    sql_parts.append(f"CREATE TABLE IF NOT EXISTS {table_name} (")
    
    # Campos
    fields = []
    for field in model._meta.fields:
        field_sql = get_field_sql(field)
        if field_sql:
            fields.append(f"    {field_sql}")
    
    sql_parts.append(",\n".join(fields))
    sql_parts.append(");")
    
    return "\n".join(sql_parts)


def get_field_sql(field):
    """Converte um campo Django para SQL PostgreSQL."""
    field_name = field.column
    field_type = ""
    constraints = []
    
    # Mapear tipos de campo
    if field.__class__.__name__ == 'AutoField':
        field_type = "SERIAL PRIMARY KEY"
    elif field.__class__.__name__ == 'BigAutoField':
        field_type = "BIGSERIAL PRIMARY KEY"
    elif field.__class__.__name__ == 'CharField':
        max_length = getattr(field, 'max_length', 255)
        field_type = f"VARCHAR({max_length})"
    elif field.__class__.__name__ == 'TextField':
        field_type = "TEXT"
    elif field.__class__.__name__ == 'EmailField':
        field_type = "VARCHAR(254)"
    elif field.__class__.__name__ == 'IntegerField':
        field_type = "INTEGER"
    elif field.__class__.__name__ == 'BigIntegerField':
        field_type = "BIGINT"
    elif field.__class__.__name__ == 'DecimalField':
        digits = getattr(field, 'max_digits', 10)
        decimal_places = getattr(field, 'decimal_places', 2)
        field_type = f"DECIMAL({digits},{decimal_places})"
    elif field.__class__.__name__ == 'FloatField':
        field_type = "DOUBLE PRECISION"
    elif field.__class__.__name__ == 'BooleanField':
        field_type = "BOOLEAN"
    elif field.__class__.__name__ == 'DateField':
        field_type = "DATE"
    elif field.__class__.__name__ == 'DateTimeField':
        field_type = "TIMESTAMP WITH TIME ZONE"
    elif field.__class__.__name__ == 'TimeField':
        field_type = "TIME"
    elif field.__class__.__name__ == 'ForeignKey':
        field_type = "INTEGER"
        # Adicionar constraint de FK depois
    elif field.__class__.__name__ == 'ImageField' or field.__class__.__name__ == 'FileField':
        field_type = "VARCHAR(100)"
    else:
        field_type = "TEXT"  # Default
    
    # Constraints
    if not field.null:
        constraints.append("NOT NULL")
    
    if field.unique:
        constraints.append("UNIQUE")
    
    if hasattr(field, 'default') and field.default is not None:
        if callable(field.default):
            pass  # Não adicionar defaults de função
        elif isinstance(field.default, bool):
            constraints.append(f"DEFAULT {str(field.default).upper()}")
        elif isinstance(field.default, str):
            constraints.append(f"DEFAULT '{field.default}'")
        else:
            constraints.append(f"DEFAULT {field.default}")
    
    # Montar SQL final
    constraints_str = " " + " ".join(constraints) if constraints else ""
    return f"{field_name} {field_type}{constraints_str}"


def count_lines(file_path):
    """Conta o número de linhas em um arquivo."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)


if __name__ == "__main__":
    from datetime import datetime
    
    try:
        schema_file = generate_postgresql_schema()
        
        print(f"\n🎉 Script concluído com sucesso!")
        print(f"📁 Arquivo gerado: {schema_file}")
        print(f"\n📋 Para usar:")
        print(f"1. Instale PostgreSQL no seu sistema")
        print(f"2. Execute: psql -U postgres -f {schema_file.name}")
        print(f"3. Configure seu .env com as credenciais do banco")
        print(f"4. Execute: python manage.py migrate")
        
    except Exception as e:
        print(f"❌ Erro ao gerar estrutura: {e}")
        sys.exit(1)
