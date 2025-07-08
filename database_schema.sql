-- =====================================================
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
--    \q
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


-- Tabela de migrações
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


-- =====================================================
-- ACCOUNTS APP
-- =====================================================

-- Tabela: User
CREATE TABLE "accounts_user" (
    "id" BIGSERIAL PRIMARY KEY,
    "password" VARCHAR(128) NOT NULL,
    "last_login" TIMESTAMP WITH TIME ZONE,
    "is_superuser" BOOLEAN NOT NULL DEFAULT FALSE,
    "username" VARCHAR(150) NOT NULL UNIQUE,
    "first_name" VARCHAR(150) NOT NULL,
    "last_name" VARCHAR(150) NOT NULL,
    "is_staff" BOOLEAN NOT NULL DEFAULT FALSE,
    "is_active" BOOLEAN NOT NULL DEFAULT TRUE,
    "date_joined" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT <function now at 0x10614d550>,
    "email" VARCHAR(254) NOT NULL UNIQUE,
    "telefone" VARCHAR(20) NOT NULL,
    "foto_perfil" VARCHAR(100),
    "data_nascimento" DATE,
    "cref" VARCHAR(20) NOT NULL,
    "bio" TEXT NOT NULL,
    "data_criacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    "data_atualizacao" TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela M2M: groups
CREATE TABLE "accounts_user_groups" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INTEGER NOT NULL,
    "group_id" INTEGER NOT NULL,
    CONSTRAINT "fk_accounts_user_groups_user_id" FOREIGN KEY ("user_id") REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_accounts_user_groups_group_id" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "group_id")
);

-- Tabela M2M: user_permissions
CREATE TABLE "accounts_user_user_permissions" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INTEGER NOT NULL,
    "permission_id" INTEGER NOT NULL,
    CONSTRAINT "fk_accounts_user_user_permissions_user_id" FOREIGN KEY ("user_id") REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_accounts_user_user_permissions_permission_id" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("user_id", "permission_id")
);


-- =====================================================
-- ALUNOS APP
-- =====================================================

-- Tabela: Aluno
CREATE TABLE "alunos_aluno" (
    "id" BIGSERIAL PRIMARY KEY,
    "nome" VARCHAR(200) NOT NULL,
    "email" VARCHAR(254) NOT NULL UNIQUE,
    "telefone" VARCHAR(20) NOT NULL,
    "data_nascimento" DATE NOT NULL,
    "sexo" VARCHAR(1) NOT NULL,
    "endereco" TEXT NOT NULL,
    "peso_inicial" DECIMAL(5,2) NOT NULL,
    "altura" DECIMAL(4,2) NOT NULL,
    "objetivo" VARCHAR(20) NOT NULL,
    "observacoes" TEXT NOT NULL,
    "personal_trainer_id" INTEGER NOT NULL,
    "ativo" BOOLEAN NOT NULL DEFAULT TRUE,
    "data_inicio" DATE NOT NULL DEFAULT <function now at 0x10614d550>,
    "data_criacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    "data_atualizacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT "fk_alunos_aluno_personal_trainer_id" FOREIGN KEY ("personal_trainer_id") REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: MedidasCorporais
CREATE TABLE "alunos_medidascorporais" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL,
    "data_medicao" DATE NOT NULL DEFAULT <function now at 0x10614d550>,
    "peso" DECIMAL(5,2) NOT NULL,
    "percentual_gordura" DECIMAL(4,1),
    "pescoco" DECIMAL(4,1),
    "torax" DECIMAL(4,1),
    "cintura" DECIMAL(4,1),
    "quadril" DECIMAL(4,1),
    "braco_direito" DECIMAL(4,1),
    "braco_esquerdo" DECIMAL(4,1),
    "coxa_direita" DECIMAL(4,1),
    "coxa_esquerda" DECIMAL(4,1),
    "observacoes" TEXT NOT NULL,
    CONSTRAINT "fk_alunos_medidascorporais_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: FotoProgresso
CREATE TABLE "alunos_fotoprogresso" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL,
    "data_foto" DATE NOT NULL DEFAULT <function now at 0x10614d550>,
    "tipo_foto" VARCHAR(10) NOT NULL,
    "foto" VARCHAR(100) NOT NULL,
    "descricao" VARCHAR(200) NOT NULL,
    CONSTRAINT "fk_alunos_fotoprogresso_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED
);


-- =====================================================
-- TREINOS APP
-- =====================================================

-- Tabela: Exercicio
CREATE TABLE "treinos_exercicio" (
    "id" BIGSERIAL PRIMARY KEY,
    "nome" VARCHAR(200) NOT NULL,
    "descricao" TEXT NOT NULL,
    "grupo_muscular" VARCHAR(20) NOT NULL,
    "categoria" VARCHAR(20) NOT NULL,
    "equipamento" VARCHAR(20) NOT NULL DEFAULT 'livre',
    "instrucoes" TEXT NOT NULL,
    "video_url" VARCHAR(200) NOT NULL,
    "imagem" VARCHAR(100)
);

-- Tabela: PlanoTreino
CREATE TABLE "treinos_planotreino" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL,
    "nome" VARCHAR(200) NOT NULL,
    "descricao" TEXT NOT NULL,
    "data_inicio" DATE NOT NULL DEFAULT <function now at 0x10614d550>,
    "data_fim" DATE,
    "duracao_semanas" INTEGER NOT NULL DEFAULT 4,
    "ativo" BOOLEAN NOT NULL DEFAULT TRUE,
    "observacoes" TEXT NOT NULL,
    "data_criacao" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT <function now at 0x10614d550>,
    "personal_trainer_id" INTEGER,
    CONSTRAINT "fk_treinos_planotreino_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_treinos_planotreino_personal_trainer_id" FOREIGN KEY ("personal_trainer_id") REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: TreinoDiario
CREATE TABLE "treinos_treinodiario" (
    "id" BIGSERIAL PRIMARY KEY,
    "plano_treino_id" INTEGER NOT NULL,
    "dia_semana" VARCHAR(10) NOT NULL,
    "nome" VARCHAR(200) NOT NULL,
    "descricao" TEXT NOT NULL,
    "tempo_estimado" INTEGER,
    "observacoes" TEXT NOT NULL,
    CONSTRAINT "fk_treinos_treinodiario_plano_treino_id" FOREIGN KEY ("plano_treino_id") REFERENCES "treinos_planotreino" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: ExercicioTreino
CREATE TABLE "treinos_exerciciotreino" (
    "id" BIGSERIAL PRIMARY KEY,
    "treino_diario_id" INTEGER NOT NULL,
    "exercicio_id" INTEGER NOT NULL,
    "ordem" INTEGER NOT NULL,
    "series" INTEGER NOT NULL,
    "repeticoes" VARCHAR(50) NOT NULL,
    "carga" VARCHAR(50) NOT NULL,
    "tempo_descanso" VARCHAR(50) NOT NULL,
    "observacoes" TEXT NOT NULL,
    CONSTRAINT "fk_treinos_exerciciotreino_treino_diario_id" FOREIGN KEY ("treino_diario_id") REFERENCES "treinos_treinodiario" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_treinos_exerciciotreino_exercicio_id" FOREIGN KEY ("exercicio_id") REFERENCES "treinos_exercicio" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: RegistroTreino
CREATE TABLE "treinos_registrotreino" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL,
    "treino_diario_id" INTEGER NOT NULL,
    "data_execucao" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT <function now at 0x10614d550>,
    "tempo_total" INTEGER,
    "observacoes" TEXT NOT NULL,
    "avaliacoes" INTEGER,
    CONSTRAINT "fk_treinos_registrotreino_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_treinos_registrotreino_treino_diario_id" FOREIGN KEY ("treino_diario_id") REFERENCES "treinos_treinodiario" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: RegistroExercicio
CREATE TABLE "treinos_registroexercicio" (
    "id" BIGSERIAL PRIMARY KEY,
    "registro_treino_id" INTEGER NOT NULL,
    "exercicio_treino_id" INTEGER NOT NULL,
    "series_executadas" INTEGER NOT NULL,
    "repeticoes_executadas" VARCHAR(200) NOT NULL,
    "carga_utilizada" VARCHAR(50) NOT NULL,
    "observacoes" TEXT NOT NULL,
    CONSTRAINT "fk_treinos_registroexercicio_registro_treino_id" FOREIGN KEY ("registro_treino_id") REFERENCES "treinos_registrotreino" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_treinos_registroexercicio_exercicio_treino_id" FOREIGN KEY ("exercicio_treino_id") REFERENCES "treinos_exerciciotreino" ("id") DEFERRABLE INITIALLY DEFERRED
);


-- =====================================================
-- FREQUENCIA APP
-- =====================================================

-- Tabela: RegistroPresenca
CREATE TABLE "frequencia_registropresenca" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL,
    "data_aula" DATE NOT NULL DEFAULT <function now at 0x10614d550>,
    "horario_inicio" TIME NOT NULL,
    "horario_fim" TIME,
    "status" VARCHAR(20) NOT NULL,
    "observacoes" TEXT NOT NULL,
    "data_registro" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT "fk_frequencia_registropresenca_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: AgendaAula
CREATE TABLE "frequencia_agendaaula" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL,
    "data_aula" DATE NOT NULL,
    "horario_inicio" TIME NOT NULL,
    "horario_fim" TIME NOT NULL,
    "status" VARCHAR(15) NOT NULL DEFAULT 'agendado',
    "tipo_treino" VARCHAR(200) NOT NULL,
    "observacoes" TEXT NOT NULL,
    "data_criacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    "data_atualizacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT "fk_frequencia_agendaaula_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: RelatorioFrequencia
CREATE TABLE "frequencia_relatoriofrequencia" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL,
    "mes" INTEGER NOT NULL,
    "ano" INTEGER NOT NULL,
    "total_aulas_agendadas" INTEGER NOT NULL DEFAULT 0,
    "total_presencas" INTEGER NOT NULL DEFAULT 0,
    "total_faltas" INTEGER NOT NULL DEFAULT 0,
    "total_faltas_justificadas" INTEGER NOT NULL DEFAULT 0,
    "percentual_frequencia" DECIMAL(5,2) NOT NULL DEFAULT 0,
    "data_geracao" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT "fk_frequencia_relatoriofrequencia_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED
);


-- =====================================================
-- FINANCEIRO APP
-- =====================================================

-- Tabela: PlanoMensalidade
CREATE TABLE "financeiro_planomensalidade" (
    "id" BIGSERIAL PRIMARY KEY,
    "nome" VARCHAR(200) NOT NULL,
    "descricao" TEXT NOT NULL,
    "valor" DECIMAL(8,2) NOT NULL,
    "aulas_incluidas" INTEGER NOT NULL,
    "ativo" BOOLEAN NOT NULL DEFAULT TRUE,
    "data_criacao" TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: ContratoAluno
CREATE TABLE "financeiro_contratoaluno" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL UNIQUE,
    "plano_mensalidade_id" INTEGER NOT NULL,
    "valor_personalizado" DECIMAL(8,2),
    "dia_vencimento" INTEGER NOT NULL DEFAULT 5,
    "ativo" BOOLEAN NOT NULL DEFAULT TRUE,
    "data_inicio" DATE NOT NULL DEFAULT <function now at 0x10614d550>,
    "data_fim" DATE,
    "observacoes" TEXT NOT NULL,
    CONSTRAINT "fk_financeiro_contratoaluno_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_financeiro_contratoaluno_plano_mensalidade_id" FOREIGN KEY ("plano_mensalidade_id") REFERENCES "financeiro_planomensalidade" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: Fatura
CREATE TABLE "financeiro_fatura" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL,
    "contrato_id" INTEGER NOT NULL,
    "mes_referencia" INTEGER NOT NULL,
    "ano_referencia" INTEGER NOT NULL,
    "valor_original" DECIMAL(8,2) NOT NULL,
    "desconto" DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    "acrescimo" DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    "valor_final" DECIMAL(8,2) NOT NULL,
    "data_vencimento" DATE NOT NULL,
    "status" VARCHAR(15) NOT NULL DEFAULT 'pendente',
    "observacoes" TEXT NOT NULL,
    "data_criacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    "data_atualizacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT "fk_financeiro_fatura_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_financeiro_fatura_contrato_id" FOREIGN KEY ("contrato_id") REFERENCES "financeiro_contratoaluno" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: Pagamento
CREATE TABLE "financeiro_pagamento" (
    "id" BIGSERIAL PRIMARY KEY,
    "fatura_id" INTEGER NOT NULL,
    "data_pagamento" DATE NOT NULL DEFAULT <function now at 0x10614d550>,
    "valor_pago" DECIMAL(8,2) NOT NULL,
    "forma_pagamento" VARCHAR(20) NOT NULL,
    "observacoes" TEXT NOT NULL,
    "comprovante" VARCHAR(100),
    "data_registro" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT "fk_financeiro_pagamento_fatura_id" FOREIGN KEY ("fatura_id") REFERENCES "financeiro_fatura" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: RelatorioFinanceiro
CREATE TABLE "financeiro_relatoriofinanceiro" (
    "id" BIGSERIAL PRIMARY KEY,
    "mes" INTEGER NOT NULL,
    "ano" INTEGER NOT NULL,
    "total_faturado" DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    "total_recebido" DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    "total_pendente" DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    "total_atrasado" DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    "numero_alunos_ativos" INTEGER NOT NULL DEFAULT 0,
    "numero_faturas_pagas" INTEGER NOT NULL DEFAULT 0,
    "numero_faturas_pendentes" INTEGER NOT NULL DEFAULT 0,
    "data_geracao" TIMESTAMP WITH TIME ZONE NOT NULL
);


-- =====================================================
-- RELATORIOS APP
-- =====================================================

-- Tabela: TipoRelatorio
CREATE TABLE "relatorios_tiporelatorio" (
    "id" BIGSERIAL PRIMARY KEY,
    "nome" VARCHAR(100) NOT NULL,
    "descricao" TEXT NOT NULL,
    "template_filename" VARCHAR(200) NOT NULL,
    "ativo" BOOLEAN NOT NULL DEFAULT TRUE,
    "incluir_graficos" BOOLEAN NOT NULL DEFAULT TRUE,
    "incluir_fotos" BOOLEAN NOT NULL DEFAULT TRUE,
    "incluir_medidas" BOOLEAN NOT NULL DEFAULT TRUE,
    "incluir_frequencia" BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela: RelatorioProgresso
CREATE TABLE "relatorios_relatorioprogresso" (
    "id" TEXT DEFAULT <function uuid4 at 0x105f20670>,
    "aluno_id" INTEGER NOT NULL,
    "tipo_relatorio_id" INTEGER NOT NULL,
    "personal_trainer_id" INTEGER NOT NULL,
    "titulo" VARCHAR(200) NOT NULL,
    "periodo" VARCHAR(15) NOT NULL,
    "data_inicio" DATE NOT NULL,
    "data_fim" DATE NOT NULL,
    "status" VARCHAR(15) NOT NULL DEFAULT 'gerando',
    "arquivo_pdf" VARCHAR(100),
    "peso_inicial" DECIMAL(5,2),
    "peso_final" DECIMAL(5,2),
    "diferenca_peso" DECIMAL(5,2),
    "imc_inicial" DECIMAL(4,2),
    "imc_final" DECIMAL(4,2),
    "total_treinos" INTEGER NOT NULL DEFAULT 0,
    "percentual_frequencia" DECIMAL(5,2) NOT NULL DEFAULT 0,
    "observacoes" TEXT NOT NULL,
    "data_geracao" TIMESTAMP WITH TIME ZONE NOT NULL,
    "data_atualizacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT "fk_relatorios_relatorioprogresso_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_relatorios_relatorioprogresso_tipo_relatorio_id" FOREIGN KEY ("tipo_relatorio_id") REFERENCES "relatorios_tiporelatorio" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_relatorios_relatorioprogresso_personal_trainer_id" FOREIGN KEY ("personal_trainer_id") REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: DadosRelatorio
CREATE TABLE "relatorios_dadosrelatorio" (
    "id" BIGSERIAL PRIMARY KEY,
    "relatorio_id" INTEGER NOT NULL,
    "data" DATE NOT NULL,
    "peso" DECIMAL(5,2),
    "percentual_gordura" DECIMAL(4,1),
    "medidas_json" TEXT,
    "treinos_realizados" INTEGER NOT NULL DEFAULT 0,
    "observacoes" TEXT NOT NULL,
    CONSTRAINT "fk_relatorios_dadosrelatorio_relatorio_id" FOREIGN KEY ("relatorio_id") REFERENCES "relatorios_relatorioprogresso" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: TemplateRelatorio
CREATE TABLE "relatorios_templaterelatorio" (
    "id" BIGSERIAL PRIMARY KEY,
    "nome" VARCHAR(100) NOT NULL,
    "descricao" TEXT NOT NULL,
    "conteudo_html" TEXT NOT NULL,
    "css_personalizado" TEXT NOT NULL,
    "ativo" BOOLEAN NOT NULL DEFAULT TRUE,
    "data_criacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    "data_atualizacao" TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: CompartilhamentoRelatorio
CREATE TABLE "relatorios_compartilhamentorelatorio" (
    "id" BIGSERIAL PRIMARY KEY,
    "relatorio_id" INTEGER NOT NULL,
    "token" TEXT NOT NULL DEFAULT <function uuid4 at 0x105f20670> UNIQUE,
    "email_compartilhado" VARCHAR(254) NOT NULL,
    "data_expiracao" TIMESTAMP WITH TIME ZONE NOT NULL,
    "status" VARCHAR(10) NOT NULL DEFAULT 'ativo',
    "acessos" INTEGER NOT NULL DEFAULT 0,
    "data_criacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    "ultimo_acesso" TIMESTAMP WITH TIME ZONE,
    CONSTRAINT "fk_relatorios_compartilhamentorelatorio_relatorio_id" FOREIGN KEY ("relatorio_id") REFERENCES "relatorios_relatorioprogresso" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: EstatisticaRelatorio
CREATE TABLE "relatorios_estatisticarelatorio" (
    "id" BIGSERIAL PRIMARY KEY,
    "personal_trainer_id" INTEGER NOT NULL,
    "mes" INTEGER NOT NULL,
    "ano" INTEGER NOT NULL,
    "total_relatorios_gerados" INTEGER NOT NULL DEFAULT 0,
    "total_relatorios_enviados" INTEGER NOT NULL DEFAULT 0,
    "total_downloads" INTEGER NOT NULL DEFAULT 0,
    "total_compartilhamentos" INTEGER NOT NULL DEFAULT 0,
    "relatorio_mais_gerado" VARCHAR(200) NOT NULL,
    "periodo_mais_usado" VARCHAR(15) NOT NULL,
    "data_geracao" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT "fk_relatorios_estatisticarelatorio_personal_trainer_id" FOREIGN KEY ("personal_trainer_id") REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);


-- =====================================================
-- NOTIFICACOES APP
-- =====================================================

-- Tabela: TipoNotificacao
CREATE TABLE "notificacoes_tiponotificacao" (
    "id" BIGSERIAL PRIMARY KEY,
    "nome" VARCHAR(100) NOT NULL,
    "descricao" TEXT NOT NULL,
    "cor" VARCHAR(7) NOT NULL DEFAULT '#6B7280',
    "template_titulo" VARCHAR(200) NOT NULL,
    "template_mensagem" TEXT NOT NULL,
    "ativo" BOOLEAN NOT NULL DEFAULT TRUE,
    "enviar_email" BOOLEAN NOT NULL DEFAULT FALSE,
    "enviar_whatsapp" BOOLEAN NOT NULL DEFAULT FALSE,
    "enviar_sistema" BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela: Notificacao
CREATE TABLE "notificacoes_notificacao" (
    "id" BIGSERIAL PRIMARY KEY,
    "tipo_notificacao_id" INTEGER NOT NULL,
    "personal_trainer_id" INTEGER NOT NULL,
    "aluno_id" INTEGER,
    "titulo" VARCHAR(200) NOT NULL,
    "mensagem" TEXT NOT NULL,
    "prioridade" VARCHAR(10) NOT NULL DEFAULT 'normal',
    "status" VARCHAR(15) NOT NULL DEFAULT 'pendente',
    "data_criacao" TIMESTAMP WITH TIME ZONE NOT NULL,
    "data_agendamento" TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT <function now at 0x10614d550>,
    "data_envio" TIMESTAMP WITH TIME ZONE,
    "data_leitura" TIMESTAMP WITH TIME ZONE,
    "enviado_email" BOOLEAN NOT NULL DEFAULT FALSE,
    "enviado_whatsapp" BOOLEAN NOT NULL DEFAULT FALSE,
    "enviado_sistema" BOOLEAN NOT NULL DEFAULT FALSE,
    "erro_envio" TEXT NOT NULL,
    CONSTRAINT "fk_notificacoes_notificacao_tipo_notificacao_id" FOREIGN KEY ("tipo_notificacao_id") REFERENCES "notificacoes_tiponotificacao" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_notificacoes_notificacao_personal_trainer_id" FOREIGN KEY ("personal_trainer_id") REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "fk_notificacoes_notificacao_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: NotificacaoAutomatica
CREATE TABLE "notificacoes_notificacaoautomatica" (
    "id" BIGSERIAL PRIMARY KEY,
    "nome" VARCHAR(200) NOT NULL,
    "trigger" VARCHAR(30) NOT NULL UNIQUE,
    "tipo_notificacao_id" INTEGER NOT NULL,
    "ativa" BOOLEAN NOT NULL DEFAULT TRUE,
    "antecedencia_dias" INTEGER NOT NULL DEFAULT 0,
    "horario_envio" TIME NOT NULL DEFAULT 00:39:22.897903,
    "apenas_alunos_ativos" BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT "fk_notificacoes_notificacaoautomatica_tipo_notificacao_id" FOREIGN KEY ("tipo_notificacao_id") REFERENCES "notificacoes_tiponotificacao" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: LogEnvioWhatsApp
CREATE TABLE "notificacoes_logenviowhatsapp" (
    "id" BIGSERIAL PRIMARY KEY,
    "notificacao_id" INTEGER NOT NULL,
    "telefone_destino" VARCHAR(20) NOT NULL,
    "mensagem_enviada" TEXT NOT NULL,
    "status" VARCHAR(10) NOT NULL,
    "response_api" TEXT,
    "tentativas" INTEGER NOT NULL DEFAULT 1,
    "data_envio" TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT "fk_notificacoes_logenviowhatsapp_notificacao_id" FOREIGN KEY ("notificacao_id") REFERENCES "notificacoes_notificacao" ("id") DEFERRABLE INITIALLY DEFERRED
);

-- Tabela: ConfiguracaoNotificacao
CREATE TABLE "notificacoes_configuracaonotificacao" (
    "id" BIGSERIAL PRIMARY KEY,
    "aluno_id" INTEGER NOT NULL UNIQUE,
    "receber_email" BOOLEAN NOT NULL DEFAULT TRUE,
    "receber_whatsapp" BOOLEAN NOT NULL DEFAULT TRUE,
    "receber_lembrete_pagamento" BOOLEAN NOT NULL DEFAULT TRUE,
    "receber_lembrete_treino" BOOLEAN NOT NULL DEFAULT TRUE,
    "receber_relatorio_progresso" BOOLEAN NOT NULL DEFAULT TRUE,
    "horario_preferencial" TIME NOT NULL DEFAULT 00:39:22.898774,
    "dias_antecedencia_pagamento" INTEGER NOT NULL DEFAULT 3,
    "email_alternativo" VARCHAR(254) NOT NULL,
    "telefone_alternativo" VARCHAR(20) NOT NULL,
    CONSTRAINT "fk_notificacoes_configuracaonotificacao_aluno_id" FOREIGN KEY ("aluno_id") REFERENCES "alunos_aluno" ("id") DEFERRABLE INITIALLY DEFERRED
);


-- =====================================================
-- ÍNDICES
-- =====================================================

CREATE INDEX "idx_accounts_user_groups_user_id" ON "accounts_user_groups" ("user_id");
CREATE INDEX "idx_accounts_user_groups_group_id" ON "accounts_user_groups" ("group_id");
CREATE INDEX "idx_accounts_user_user_permissions_user_id" ON "accounts_user_user_permissions" ("user_id");
CREATE INDEX "idx_accounts_user_user_permissions_permission_id" ON "accounts_user_user_permissions" ("permission_id");
CREATE INDEX "idx_alunos_aluno_personal_trainer_id" ON "alunos_aluno" ("personal_trainer_id");
CREATE INDEX "idx_alunos_medidascorporais_aluno_id" ON "alunos_medidascorporais" ("aluno_id");
CREATE INDEX "idx_alunos_fotoprogresso_aluno_id" ON "alunos_fotoprogresso" ("aluno_id");
CREATE INDEX "idx_treinos_planotreino_aluno_id" ON "treinos_planotreino" ("aluno_id");
CREATE INDEX "idx_treinos_planotreino_personal_trainer_id" ON "treinos_planotreino" ("personal_trainer_id");
CREATE INDEX "idx_treinos_treinodiario_plano_treino_id" ON "treinos_treinodiario" ("plano_treino_id");
CREATE INDEX "idx_treinos_exerciciotreino_treino_diario_id" ON "treinos_exerciciotreino" ("treino_diario_id");
CREATE INDEX "idx_treinos_exerciciotreino_exercicio_id" ON "treinos_exerciciotreino" ("exercicio_id");
CREATE INDEX "idx_treinos_registrotreino_aluno_id" ON "treinos_registrotreino" ("aluno_id");
CREATE INDEX "idx_treinos_registrotreino_treino_diario_id" ON "treinos_registrotreino" ("treino_diario_id");
CREATE INDEX "idx_treinos_registroexercicio_registro_treino_id" ON "treinos_registroexercicio" ("registro_treino_id");
CREATE INDEX "idx_treinos_registroexercicio_exercicio_treino_id" ON "treinos_registroexercicio" ("exercicio_treino_id");
CREATE INDEX "idx_frequencia_registropresenca_aluno_id" ON "frequencia_registropresenca" ("aluno_id");
CREATE INDEX "idx_frequencia_agendaaula_aluno_id" ON "frequencia_agendaaula" ("aluno_id");
CREATE INDEX "idx_frequencia_relatoriofrequencia_aluno_id" ON "frequencia_relatoriofrequencia" ("aluno_id");
CREATE INDEX "idx_financeiro_contratoaluno_aluno_id" ON "financeiro_contratoaluno" ("aluno_id");
CREATE INDEX "idx_financeiro_contratoaluno_plano_mensalidade_id" ON "financeiro_contratoaluno" ("plano_mensalidade_id");
CREATE INDEX "idx_financeiro_fatura_aluno_id" ON "financeiro_fatura" ("aluno_id");
CREATE INDEX "idx_financeiro_fatura_contrato_id" ON "financeiro_fatura" ("contrato_id");
CREATE INDEX "idx_financeiro_pagamento_fatura_id" ON "financeiro_pagamento" ("fatura_id");
CREATE INDEX "idx_relatorios_relatorioprogresso_aluno_id" ON "relatorios_relatorioprogresso" ("aluno_id");
CREATE INDEX "idx_relatorios_relatorioprogresso_tipo_relatorio_id" ON "relatorios_relatorioprogresso" ("tipo_relatorio_id");
CREATE INDEX "idx_relatorios_relatorioprogresso_personal_trainer_id" ON "relatorios_relatorioprogresso" ("personal_trainer_id");
CREATE INDEX "idx_relatorios_dadosrelatorio_relatorio_id" ON "relatorios_dadosrelatorio" ("relatorio_id");
CREATE INDEX "idx_relatorios_compartilhamentorelatorio_relatorio_id" ON "relatorios_compartilhamentorelatorio" ("relatorio_id");
CREATE INDEX "idx_relatorios_estatisticarelatorio_personal_trainer_id" ON "relatorios_estatisticarelatorio" ("personal_trainer_id");
CREATE INDEX "idx_notificacoes_notificacao_tipo_notificacao_id" ON "notificacoes_notificacao" ("tipo_notificacao_id");
CREATE INDEX "idx_notificacoes_notificacao_personal_trainer_id" ON "notificacoes_notificacao" ("personal_trainer_id");
CREATE INDEX "idx_notificacoes_notificacao_aluno_id" ON "notificacoes_notificacao" ("aluno_id");
CREATE INDEX "idx_notificacoes_notificacaoautomatica_tipo_notificacao_id" ON "notificacoes_notificacaoautomatica" ("tipo_notificacao_id");
CREATE INDEX "idx_notificacoes_logenviowhatsapp_notificacao_id" ON "notificacoes_logenviowhatsapp" ("notificacao_id");
CREATE INDEX "idx_notificacoes_configuracaonotificacao_aluno_id" ON "notificacoes_configuracaonotificacao" ("aluno_id");

-- =====================================================
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
