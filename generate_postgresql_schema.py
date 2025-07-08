#!/usr/bin/env python
"""
Script para gerar a estrutura SQL PostgreSQL do FormaFit
baseada nos modelos Django, sem precisar conectar ao banco.
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django para usar SQLite temporariamente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formafit.settings')
os.environ['USE_SQLITE'] = 'True'

django.setup()

from django.apps import apps
from django.db import models

def get_postgresql_type(field):
    """Converte tipos Django para PostgreSQL"""
    field_type = type(field).__name__
    
    if field_type == 'AutoField':
        return 'SERIAL PRIMARY KEY'
    elif field_type == 'BigAutoField':
        return 'BIGSERIAL PRIMARY KEY'
    elif field_type == 'CharField':
        max_length = getattr(field, 'max_length', 255)
        return f'VARCHAR({max_length})'
    elif field_type == 'TextField':
        return 'TEXT'
    elif field_type == 'IntegerField':
        return 'INTEGER'
    elif field_type == 'BigIntegerField':
        return 'BIGINT'
    elif field_type == 'SmallIntegerField':
        return 'SMALLINT'
    elif field_type == 'PositiveIntegerField':
        return 'INTEGER CHECK (value >= 0)'
    elif field_type == 'PositiveSmallIntegerField':
        return 'SMALLINT CHECK (value >= 0)'
    elif field_type == 'DecimalField':
        max_digits = getattr(field, 'max_digits', 10)
        decimal_places = getattr(field, 'decimal_places', 2)
        return f'DECIMAL({max_digits},{decimal_places})'
    elif field_type == 'FloatField':
        return 'DOUBLE PRECISION'
    elif field_type == 'BooleanField':
        return 'BOOLEAN'
    elif field_type == 'DateField':
        return 'DATE'
    elif field_type == 'DateTimeField':
        return 'TIMESTAMP WITH TIME ZONE'
    elif field_type == 'TimeField':
        return 'TIME'
    elif field_type == 'EmailField':
        max_length = getattr(field, 'max_length', 254)
        return f'VARCHAR({max_length})'
    elif field_type == 'URLField':
        max_length = getattr(field, 'max_length', 200)
        return f'VARCHAR({max_length})'
    elif field_type == 'FileField' or field_type == 'ImageField':
        return 'VARCHAR(100)'
    elif field_type == 'ForeignKey':
        return 'INTEGER'
    elif field_type == 'OneToOneField':
        return 'INTEGER'
    elif field_type == 'ManyToManyField':
        return None  # Handled separately
    else:
        return 'TEXT'  # Fallback

def generate_table_sql(model):
    """Gera SQL CREATE TABLE para um modelo Django"""
    table_name = model._meta.db_table
    fields = []
    foreign_keys = []
    indexes = []
    
    # Processar campos
    for field in model._meta.fields:
        field_name = field.column
        field_type = get_postgresql_type(field)
        
        if field_type is None:
            continue
            
        field_sql = f'    "{field_name}" {field_type}'
        
        # NOT NULL
        if not field.null and not field.primary_key:
            field_sql += ' NOT NULL'
            
        # DEFAULT
        if field.has_default() and field.default is not models.NOT_PROVIDED:
            if isinstance(field.default, str):
                field_sql += f" DEFAULT '{field.default}'"
            elif isinstance(field.default, bool):
                field_sql += f" DEFAULT {'TRUE' if field.default else 'FALSE'}"
            elif field.default is not None:
                field_sql += f" DEFAULT {field.default}"
        
        # UNIQUE
        if field.unique and not field.primary_key:
            field_sql += ' UNIQUE'
            
        fields.append(field_sql)
        
        # Foreign keys
        if hasattr(field, 'related_model') and field.related_model:
            fk_table = field.related_model._meta.db_table
            fk_column = field.related_model._meta.pk.column
            foreign_keys.append(
                f'    CONSTRAINT "fk_{table_name}_{field_name}" '
                f'FOREIGN KEY ("{field_name}") REFERENCES "{fk_table}" ("{fk_column}") DEFERRABLE INITIALLY DEFERRED'
            )
            indexes.append(f'CREATE INDEX "idx_{table_name}_{field_name}" ON "{table_name}" ("{field_name}");')
    
    # Montar CREATE TABLE
    sql = f'CREATE TABLE "{table_name}" (\n'
    sql += ',\n'.join(fields)
    
    if foreign_keys:
        sql += ',\n' + ',\n'.join(foreign_keys)
    
    sql += '\n);\n'
    
    return sql, indexes

def generate_m2m_table_sql(field, model):
    """Gera SQL para tabelas many-to-many"""
    through_model = field.remote_field.through
    if through_model._meta.auto_created:
        table_name = through_model._meta.db_table
        source_column = field.m2m_column_name()
        target_column = field.m2m_reverse_name()
        source_table = model._meta.db_table
        target_table = field.related_model._meta.db_table
        
        sql = f'''CREATE TABLE "{table_name}" (
    "id" SERIAL PRIMARY KEY,
    "{source_column}" INTEGER NOT NULL,
    "{target_column}" INTEGER NOT NULL,
    CONSTRAINT "fk_{table_name}_{source_column}" FOREIGN KEY ("{source_column}") REFERENCES "{source_table}" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_{table_name}_{target_column}" FOREIGN KEY ("{target_column}") REFERENCES "{target_table}" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("{source_column}", "{target_column}")
);
'''
        indexes = [
            f'CREATE INDEX "idx_{table_name}_{source_column}" ON "{table_name}" ("{source_column}");',
            f'CREATE INDEX "idx_{table_name}_{target_column}" ON "{table_name}" ("{target_column}");'
        ]
        return sql, indexes
    return '', []

def generate_schema():
    """Gera o schema completo"""
    
    sql_statements = []
    
    # Header
    sql_statements.append("""-- =====================================================
-- FORMAFIT - ESTRUTURA COMPLETA DO BANCO DE DADOS
-- Sistema para Personal Trainers
-- =====================================================
-- 
-- Este arquivo contém a estrutura completa das tabelas
-- do sistema FormaFit para PostgreSQL.
--
-- INSTRUÇÕES DE USO:
-- 
-- 1. Instale PostgreSQL e inicie o serviço
-- 2. Conecte como superusuário (postgres):
--    sudo -u postgres psql
-- 
-- 3. Execute os comandos abaixo:
--    CREATE DATABASE formafit_db;
--    CREATE USER formafit_user WITH PASSWORD 'formafit123';
--    GRANT ALL PRIVILEGES ON DATABASE formafit_db TO formafit_user;
--    ALTER USER formafit_user CREATEDB;
--    \\q
--
-- 4. Importe a estrutura:
--    psql -U formafit_user -d formafit_db -f database_schema.sql
--
-- 5. Configure o .env com os dados do banco
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

-- =====================================================
-- TABELAS DO DJANGO CORE
-- =====================================================

""")
    
    # Tabelas Django core
    django_core_tables = [
        'django_migrations', 'django_content_type', 'auth_permission', 
        'auth_group', 'auth_group_permissions', 'auth_user', 
        'auth_user_groups', 'auth_user_user_permissions',
        'django_admin_log', 'django_session'
    ]
    
    sql_statements.append("""-- Tabela de migrações
CREATE TABLE "django_migrations" (
    "id" SERIAL PRIMARY KEY,
    "app" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "applied" TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela de tipos de conteúdo
CREATE TABLE "django_content_type" (
    "id" SERIAL PRIMARY KEY,
    "app_label" VARCHAR(100) NOT NULL,
    "model" VARCHAR(100) NOT NULL,
    UNIQUE ("app_label", "model")
);

-- Tabela de permissões
CREATE TABLE "auth_permission" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "content_type_id" INTEGER NOT NULL,
    "codename" VARCHAR(100) NOT NULL,
    UNIQUE ("content_type_id", "codename"),
    CONSTRAINT "fk_auth_permission_content_type" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela de grupos
CREATE TABLE "auth_group" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(150) NOT NULL UNIQUE
);

-- Tabela de permissões por grupo
CREATE TABLE "auth_group_permissions" (
    "id" SERIAL PRIMARY KEY,
    "group_id" INTEGER NOT NULL,
    "permission_id" INTEGER NOT NULL,
    UNIQUE ("group_id", "permission_id"),
    CONSTRAINT "fk_auth_group_permissions_group" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_auth_group_permissions_permission" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela de usuários
CREATE TABLE "auth_user" (
    "id" SERIAL PRIMARY KEY,
    "password" VARCHAR(128) NOT NULL,
    "last_login" TIMESTAMP WITH TIME ZONE,
    "is_superuser" BOOLEAN NOT NULL,
    "username" VARCHAR(150) NOT NULL UNIQUE,
    "first_name" VARCHAR(150) NOT NULL,
    "last_name" VARCHAR(150) NOT NULL,
    "email" VARCHAR(254) NOT NULL,
    "is_staff" BOOLEAN NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "date_joined" TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela de usuários em grupos
CREATE TABLE "auth_user_groups" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INTEGER NOT NULL,
    "group_id" INTEGER NOT NULL,
    UNIQUE ("user_id", "group_id"),
    CONSTRAINT "fk_auth_user_groups_user" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_auth_user_groups_group" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela de permissões por usuário
CREATE TABLE "auth_user_user_permissions" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INTEGER NOT NULL,
    "permission_id" INTEGER NOT NULL,
    UNIQUE ("user_id", "permission_id"),
    CONSTRAINT "fk_auth_user_user_permissions_user" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_auth_user_user_permissions_permission" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela de log do admin
CREATE TABLE "django_admin_log" (
    "id" SERIAL PRIMARY KEY,
    "action_time" TIMESTAMP WITH TIME ZONE NOT NULL,
    "object_id" TEXT,
    "object_repr" VARCHAR(200) NOT NULL,
    "action_flag" SMALLINT NOT NULL CHECK ("action_flag" >= 0),
    "change_message" TEXT NOT NULL,
    "content_type_id" INTEGER,
    "user_id" INTEGER NOT NULL,
    CONSTRAINT "fk_django_admin_log_content_type" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_django_admin_log_user" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela de sessões
CREATE TABLE "django_session" (
    "session_key" VARCHAR(40) PRIMARY KEY,
    "session_data" TEXT NOT NULL,
    "expire_date" TIMESTAMP WITH TIME ZONE NOT NULL
);

-- =====================================================
-- TABELAS DO FORMAFIT
-- =====================================================

""")
    
    # Apps do FormaFit na ordem correta
    formafit_apps = ['accounts', 'alunos', 'treinos', 'frequencia', 'financeiro', 'relatorios', 'notificacoes']
    
    all_indexes = []
    
    for app_name in formafit_apps:
        try:
            app_config = apps.get_app_config(app_name)
            models_list = app_config.get_models()
            
            if models_list:
                sql_statements.append(f"-- =====================================================")
                sql_statements.append(f"-- {app_name.upper()} APP")
                sql_statements.append(f"-- =====================================================\n")
                
                for model in models_list:
                    table_sql, table_indexes = generate_table_sql(model)
                    sql_statements.append(f"-- Tabela: {model.__name__}")
                    sql_statements.append(table_sql)
                    all_indexes.extend(table_indexes)
                    
                    # Many-to-many tables
                    for field in model._meta.many_to_many:
                        m2m_sql, m2m_indexes = generate_m2m_table_sql(field, model)
                        if m2m_sql:
                            sql_statements.append(f"-- Tabela M2M: {field.name}")
                            sql_statements.append(m2m_sql)
                            all_indexes.extend(m2m_indexes)
                
                sql_statements.append("")
                
        except Exception as e:
            print(f"Erro ao processar app {app_name}: {e}")
            continue
    
    # Adicionar índices
    if all_indexes:
        sql_statements.append("-- =====================================================")
        sql_statements.append("-- ÍNDICES")
        sql_statements.append("-- =====================================================\n")
        for index in all_indexes:
            sql_statements.append(index)
        sql_statements.append("")
    
    # Footer
    sql_statements.append("""-- =====================================================
-- CONFIGURAÇÕES FINAIS
-- =====================================================

-- Inserir dados iniciais mínimos
INSERT INTO "django_content_type" ("app_label", "model") VALUES 
    ('contenttypes', 'contenttype'),
    ('auth', 'permission'),
    ('auth', 'group'),
    ('auth', 'user'),
    ('admin', 'logentry'),
    ('sessions', 'session'),
    ('accounts', 'user'),
    ('alunos', 'aluno'),
    ('alunos', 'medidascorporais'),
    ('alunos', 'fotoprogresso'),
    ('treinos', 'exercicio'),
    ('treinos', 'planotreino'),
    ('treinos', 'treino'),
    ('frequencia', 'agenda'),
    ('financeiro', 'plano'),
    ('financeiro', 'contrato'),
    ('financeiro', 'fatura'),
    ('financeiro', 'pagamento'),
    ('relatorios', 'configuracaorelatorio'),
    ('notificacoes', 'tiponotificacao'),
    ('notificacoes', 'configuracaonotificacao'),
    ('notificacoes', 'notificacao'),
    ('notificacoes', 'notificacaoautomatica'),
    ('notificacoes', 'logwhatsapp');

-- Atualizar sequências
SELECT setval(pg_get_serial_sequence('django_content_type', 'id'), (SELECT MAX(id) FROM django_content_type));

-- =====================================================
-- INSTRUÇÕES PÓS-INSTALAÇÃO
-- =====================================================

-- Após importar este arquivo:
-- 1. Execute: python manage.py migrate --fake-initial
-- 2. Crie superusuário: python manage.py createsuperuser
-- 3. Execute os scripts de dados iniciais:
--    python criar_dados_notificacoes.py
--    python criar_notificacoes_exemplo.py

-- =====================================================
-- FIM DO ARQUIVO
-- =====================================================
""")
    
    # Escrever arquivo
    sql_file_path = os.path.join(os.path.dirname(__file__), 'database_schema.sql')
    
    with open(sql_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_statements))
    
    print(f"✅ Arquivo SQL PostgreSQL gerado: {sql_file_path}")
    print(f"📊 Total de comandos: {len(sql_statements)}")
    
    return sql_file_path

if __name__ == "__main__":
    generate_schema()
