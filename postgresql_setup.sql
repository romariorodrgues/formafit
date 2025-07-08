-- =================================================================
-- FORMAFIT - INSTALAÇÃO RÁPIDA POSTGRESQL
-- =================================================================
-- Script simplificado para instalação rápida do banco PostgreSQL
-- Execute este arquivo para criar o banco e usuário necessários
-- =================================================================

-- 1. CRIAR USUÁRIO E BANCO
-- Execute como superuser (postgres)

-- Criar usuário
CREATE USER formafit_user WITH PASSWORD 'formafit123';

-- Criar banco
CREATE DATABASE formafit_db OWNER formafit_user;

-- Dar privilégios
GRANT ALL PRIVILEGES ON DATABASE formafit_db TO formafit_user;
ALTER USER formafit_user CREATEDB;

-- Conectar ao banco
\c formafit_db;

-- Dar permissões no schema
GRANT ALL ON SCHEMA public TO formafit_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO formafit_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO formafit_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO formafit_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO formafit_user;

-- =================================================================
-- VERIFICAÇÃO
-- =================================================================

-- Verificar se o usuário foi criado
SELECT usename FROM pg_user WHERE usename = 'formafit_user';

-- Verificar se o banco foi criado
SELECT datname FROM pg_database WHERE datname = 'formafit_db';

-- =================================================================
-- INFORMAÇÕES
-- =================================================================

/*
APÓS EXECUTAR ESTE SCRIPT:

1. Configure seu arquivo .env:
   DATABASE_NAME=formafit_db
   DATABASE_USER=formafit_user
   DATABASE_PASSWORD=formafit123
   DATABASE_HOST=localhost
   DATABASE_PORT=5432

2. Execute as migrações Django:
   python manage.py migrate

3. Crie um superusuário:
   python manage.py createsuperuser

4. Execute o servidor:
   python manage.py runserver

O sistema estará pronto para uso!
*/
