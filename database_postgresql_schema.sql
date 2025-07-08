-- =================================================================
-- FORMAFIT - ESTRUTURA DO BANCO POSTGRESQL
-- =================================================================
-- Sistema completo para personal trainers
-- Gestão de alunos, treinos, frequência e finanças
-- 
-- Data de geração: 07/07/2025 21:51:21
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
\c formafit_db;

-- Dar permissões ao usuário
GRANT ALL ON SCHEMA public TO formafit_user;

-- =================================================================
-- ESTRUTURA DAS TABELAS
-- =================================================================


-- =============================================
-- APP: AUTH
-- =============================================

-- Tabela: auth_permission
CREATE TABLE IF NOT EXISTS auth_permission (
    id SERIAL PRIMARY KEY NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL
);

-- Tabela: auth_group
CREATE TABLE IF NOT EXISTS auth_group (
    id SERIAL PRIMARY KEY NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL UNIQUE
);


-- =============================================
-- APP: CONTENTTYPES
-- =============================================

-- Tabela: django_content_type
CREATE TABLE IF NOT EXISTS django_content_type (
    id SERIAL PRIMARY KEY NOT NULL UNIQUE,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL
);


-- =============================================
-- APP: SESSIONS
-- =============================================

-- Tabela: django_session
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) NOT NULL UNIQUE,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);


-- =============================================
-- APP: ADMIN
-- =============================================

-- Tabela: django_admin_log
CREATE TABLE IF NOT EXISTS django_admin_log (
    id SERIAL PRIMARY KEY NOT NULL UNIQUE,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id INTEGER NOT NULL,
    content_type_id INTEGER,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag TEXT NOT NULL,
    change_message TEXT NOT NULL
);


-- =============================================
-- APP: ACCOUNTS
-- =============================================

-- Tabela: accounts_user
CREATE TABLE IF NOT EXISTS accounts_user (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    foto_perfil VARCHAR(100),
    data_nascimento DATE,
    cref VARCHAR(20) NOT NULL,
    bio TEXT NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL,
    data_atualizacao TIMESTAMP WITH TIME ZONE NOT NULL
);


-- =============================================
-- APP: ALUNOS
-- =============================================

-- Tabela: alunos_aluno
CREATE TABLE IF NOT EXISTS alunos_aluno (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    nome VARCHAR(200) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    data_nascimento DATE NOT NULL,
    sexo VARCHAR(1) NOT NULL,
    endereco TEXT NOT NULL,
    peso_inicial DECIMAL(5,2) NOT NULL,
    altura DECIMAL(4,2) NOT NULL,
    objetivo VARCHAR(20) NOT NULL,
    observacoes TEXT NOT NULL,
    personal_trainer_id INTEGER NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_inicio DATE NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL,
    data_atualizacao TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: alunos_medidascorporais
CREATE TABLE IF NOT EXISTS alunos_medidascorporais (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id INTEGER NOT NULL,
    data_medicao DATE NOT NULL,
    peso DECIMAL(5,2) NOT NULL,
    percentual_gordura DECIMAL(4,1),
    pescoco DECIMAL(4,1),
    torax DECIMAL(4,1),
    cintura DECIMAL(4,1),
    quadril DECIMAL(4,1),
    braco_direito DECIMAL(4,1),
    braco_esquerdo DECIMAL(4,1),
    coxa_direita DECIMAL(4,1),
    coxa_esquerda DECIMAL(4,1),
    observacoes TEXT NOT NULL
);

-- Tabela: alunos_fotoprogresso
CREATE TABLE IF NOT EXISTS alunos_fotoprogresso (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id INTEGER NOT NULL,
    data_foto DATE NOT NULL,
    tipo_foto VARCHAR(10) NOT NULL,
    foto VARCHAR(100) NOT NULL,
    descricao VARCHAR(200) NOT NULL
);


-- =============================================
-- APP: TREINOS
-- =============================================

-- Tabela: treinos_exercicio
CREATE TABLE IF NOT EXISTS treinos_exercicio (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    grupo_muscular VARCHAR(20) NOT NULL,
    categoria VARCHAR(20) NOT NULL,
    equipamento VARCHAR(20) NOT NULL DEFAULT 'livre',
    instrucoes TEXT NOT NULL,
    video_url TEXT NOT NULL,
    imagem VARCHAR(100)
);

-- Tabela: treinos_planotreino
CREATE TABLE IF NOT EXISTS treinos_planotreino (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id INTEGER NOT NULL,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    duracao_semanas INTEGER NOT NULL DEFAULT 4,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    observacoes TEXT NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL,
    personal_trainer_id INTEGER
);

-- Tabela: treinos_treinodiario
CREATE TABLE IF NOT EXISTS treinos_treinodiario (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    plano_treino_id INTEGER NOT NULL,
    dia_semana VARCHAR(10) NOT NULL,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    tempo_estimado INTEGER,
    observacoes TEXT NOT NULL
);

-- Tabela: treinos_exerciciotreino
CREATE TABLE IF NOT EXISTS treinos_exerciciotreino (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    treino_diario_id INTEGER NOT NULL,
    exercicio_id INTEGER NOT NULL,
    ordem INTEGER NOT NULL,
    series INTEGER NOT NULL,
    repeticoes VARCHAR(50) NOT NULL,
    carga VARCHAR(50) NOT NULL,
    tempo_descanso VARCHAR(50) NOT NULL,
    observacoes TEXT NOT NULL
);

-- Tabela: treinos_registrotreino
CREATE TABLE IF NOT EXISTS treinos_registrotreino (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id INTEGER NOT NULL,
    treino_diario_id INTEGER NOT NULL,
    data_execucao TIMESTAMP WITH TIME ZONE NOT NULL,
    tempo_total INTEGER,
    observacoes TEXT NOT NULL,
    avaliacoes INTEGER
);

-- Tabela: treinos_registroexercicio
CREATE TABLE IF NOT EXISTS treinos_registroexercicio (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    registro_treino_id INTEGER NOT NULL,
    exercicio_treino_id INTEGER NOT NULL,
    series_executadas INTEGER NOT NULL,
    repeticoes_executadas VARCHAR(200) NOT NULL,
    carga_utilizada VARCHAR(50) NOT NULL,
    observacoes TEXT NOT NULL
);


-- =============================================
-- APP: FREQUENCIA
-- =============================================

-- Tabela: frequencia_registropresenca
CREATE TABLE IF NOT EXISTS frequencia_registropresenca (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id INTEGER NOT NULL,
    data_aula DATE NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME,
    status VARCHAR(20) NOT NULL,
    observacoes TEXT NOT NULL,
    data_registro TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: frequencia_agendaaula
CREATE TABLE IF NOT EXISTS frequencia_agendaaula (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id INTEGER NOT NULL,
    data_aula DATE NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    status VARCHAR(15) NOT NULL DEFAULT 'agendado',
    tipo_treino VARCHAR(200) NOT NULL,
    observacoes TEXT NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL,
    data_atualizacao TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: frequencia_relatoriofrequencia
CREATE TABLE IF NOT EXISTS frequencia_relatoriofrequencia (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    total_aulas_agendadas INTEGER NOT NULL DEFAULT 0,
    total_presencas INTEGER NOT NULL DEFAULT 0,
    total_faltas INTEGER NOT NULL DEFAULT 0,
    total_faltas_justificadas INTEGER NOT NULL DEFAULT 0,
    percentual_frequencia DECIMAL(5,2) NOT NULL DEFAULT 0,
    data_geracao TIMESTAMP WITH TIME ZONE NOT NULL
);


-- =============================================
-- APP: FINANCEIRO
-- =============================================

-- Tabela: financeiro_planomensalidade
CREATE TABLE IF NOT EXISTS financeiro_planomensalidade (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    nome VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    valor DECIMAL(8,2) NOT NULL,
    aulas_incluidas INTEGER NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: financeiro_contratoaluno
CREATE TABLE IF NOT EXISTS financeiro_contratoaluno (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id TEXT NOT NULL UNIQUE,
    plano_mensalidade_id INTEGER NOT NULL,
    valor_personalizado DECIMAL(8,2),
    dia_vencimento INTEGER NOT NULL DEFAULT 5,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    observacoes TEXT NOT NULL
);

-- Tabela: financeiro_fatura
CREATE TABLE IF NOT EXISTS financeiro_fatura (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id INTEGER NOT NULL,
    contrato_id INTEGER NOT NULL,
    mes_referencia INTEGER NOT NULL,
    ano_referencia INTEGER NOT NULL,
    valor_original DECIMAL(8,2) NOT NULL,
    desconto DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    acrescimo DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    valor_final DECIMAL(8,2) NOT NULL,
    data_vencimento DATE NOT NULL,
    status VARCHAR(15) NOT NULL DEFAULT 'pendente',
    observacoes TEXT NOT NULL,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL,
    data_atualizacao TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: financeiro_pagamento
CREATE TABLE IF NOT EXISTS financeiro_pagamento (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    fatura_id INTEGER NOT NULL,
    data_pagamento DATE NOT NULL,
    valor_pago DECIMAL(8,2) NOT NULL,
    forma_pagamento VARCHAR(20) NOT NULL,
    observacoes TEXT NOT NULL,
    comprovante VARCHAR(100),
    data_registro TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: financeiro_relatoriofinanceiro
CREATE TABLE IF NOT EXISTS financeiro_relatoriofinanceiro (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    total_faturado DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_recebido DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_pendente DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_atrasado DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    numero_alunos_ativos INTEGER NOT NULL DEFAULT 0,
    numero_faturas_pagas INTEGER NOT NULL DEFAULT 0,
    numero_faturas_pendentes INTEGER NOT NULL DEFAULT 0,
    data_geracao TIMESTAMP WITH TIME ZONE NOT NULL
);


-- =============================================
-- APP: RELATORIOS
-- =============================================

-- Tabela: relatorios_tiporelatorio
CREATE TABLE IF NOT EXISTS relatorios_tiporelatorio (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    template_filename VARCHAR(200) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    incluir_graficos BOOLEAN NOT NULL DEFAULT TRUE,
    incluir_fotos BOOLEAN NOT NULL DEFAULT TRUE,
    incluir_medidas BOOLEAN NOT NULL DEFAULT TRUE,
    incluir_frequencia BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela: relatorios_relatorioprogresso
CREATE TABLE IF NOT EXISTS relatorios_relatorioprogresso (
    id TEXT NOT NULL UNIQUE,
    aluno_id INTEGER NOT NULL,
    tipo_relatorio_id INTEGER NOT NULL,
    personal_trainer_id INTEGER NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    periodo VARCHAR(15) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    status VARCHAR(15) NOT NULL DEFAULT 'gerando',
    arquivo_pdf VARCHAR(100),
    peso_inicial DECIMAL(5,2),
    peso_final DECIMAL(5,2),
    diferenca_peso DECIMAL(5,2),
    imc_inicial DECIMAL(4,2),
    imc_final DECIMAL(4,2),
    total_treinos INTEGER NOT NULL DEFAULT 0,
    percentual_frequencia DECIMAL(5,2) NOT NULL DEFAULT 0,
    observacoes TEXT NOT NULL,
    data_geracao TIMESTAMP WITH TIME ZONE NOT NULL,
    data_atualizacao TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: relatorios_dadosrelatorio
CREATE TABLE IF NOT EXISTS relatorios_dadosrelatorio (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    relatorio_id INTEGER NOT NULL,
    data DATE NOT NULL,
    peso DECIMAL(5,2),
    percentual_gordura DECIMAL(4,1),
    medidas_json TEXT,
    treinos_realizados INTEGER NOT NULL DEFAULT 0,
    observacoes TEXT NOT NULL
);

-- Tabela: relatorios_templaterelatorio
CREATE TABLE IF NOT EXISTS relatorios_templaterelatorio (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    conteudo_html TEXT NOT NULL,
    css_personalizado TEXT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL,
    data_atualizacao TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: relatorios_compartilhamentorelatorio
CREATE TABLE IF NOT EXISTS relatorios_compartilhamentorelatorio (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    relatorio_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    email_compartilhado VARCHAR(254) NOT NULL,
    data_expiracao TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'ativo',
    acessos INTEGER NOT NULL DEFAULT 0,
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL,
    ultimo_acesso TIMESTAMP WITH TIME ZONE
);

-- Tabela: relatorios_estatisticarelatorio
CREATE TABLE IF NOT EXISTS relatorios_estatisticarelatorio (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    personal_trainer_id INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    ano INTEGER NOT NULL,
    total_relatorios_gerados INTEGER NOT NULL DEFAULT 0,
    total_relatorios_enviados INTEGER NOT NULL DEFAULT 0,
    total_downloads INTEGER NOT NULL DEFAULT 0,
    total_compartilhamentos INTEGER NOT NULL DEFAULT 0,
    relatorio_mais_gerado VARCHAR(200) NOT NULL,
    periodo_mais_usado VARCHAR(15) NOT NULL,
    data_geracao TIMESTAMP WITH TIME ZONE NOT NULL
);


-- =============================================
-- APP: NOTIFICACOES
-- =============================================

-- Tabela: notificacoes_tiponotificacao
CREATE TABLE IF NOT EXISTS notificacoes_tiponotificacao (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    cor VARCHAR(7) NOT NULL DEFAULT '#6B7280',
    template_titulo VARCHAR(200) NOT NULL,
    template_mensagem TEXT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    enviar_email BOOLEAN NOT NULL DEFAULT FALSE,
    enviar_whatsapp BOOLEAN NOT NULL DEFAULT FALSE,
    enviar_sistema BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela: notificacoes_notificacao
CREATE TABLE IF NOT EXISTS notificacoes_notificacao (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    tipo_notificacao_id INTEGER NOT NULL,
    personal_trainer_id INTEGER NOT NULL,
    aluno_id INTEGER,
    titulo VARCHAR(200) NOT NULL,
    mensagem TEXT NOT NULL,
    prioridade VARCHAR(10) NOT NULL DEFAULT 'normal',
    status VARCHAR(15) NOT NULL DEFAULT 'pendente',
    data_criacao TIMESTAMP WITH TIME ZONE NOT NULL,
    data_agendamento TIMESTAMP WITH TIME ZONE NOT NULL,
    data_envio TIMESTAMP WITH TIME ZONE,
    data_leitura TIMESTAMP WITH TIME ZONE,
    enviado_email BOOLEAN NOT NULL DEFAULT FALSE,
    enviado_whatsapp BOOLEAN NOT NULL DEFAULT FALSE,
    enviado_sistema BOOLEAN NOT NULL DEFAULT FALSE,
    erro_envio TEXT NOT NULL
);

-- Tabela: notificacoes_notificacaoautomatica
CREATE TABLE IF NOT EXISTS notificacoes_notificacaoautomatica (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    nome VARCHAR(200) NOT NULL,
    trigger VARCHAR(30) NOT NULL UNIQUE,
    tipo_notificacao_id INTEGER NOT NULL,
    ativa BOOLEAN NOT NULL DEFAULT TRUE,
    antecedencia_dias INTEGER NOT NULL DEFAULT 0,
    horario_envio TIME NOT NULL DEFAULT 00:51:21.013468,
    apenas_alunos_ativos BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela: notificacoes_logenviowhatsapp
CREATE TABLE IF NOT EXISTS notificacoes_logenviowhatsapp (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    notificacao_id INTEGER NOT NULL,
    telefone_destino VARCHAR(20) NOT NULL,
    mensagem_enviada TEXT NOT NULL,
    status VARCHAR(10) NOT NULL,
    response_api TEXT,
    tentativas INTEGER NOT NULL DEFAULT 1,
    data_envio TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabela: notificacoes_configuracaonotificacao
CREATE TABLE IF NOT EXISTS notificacoes_configuracaonotificacao (
    id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
    aluno_id TEXT NOT NULL UNIQUE,
    receber_email BOOLEAN NOT NULL DEFAULT TRUE,
    receber_whatsapp BOOLEAN NOT NULL DEFAULT TRUE,
    receber_lembrete_pagamento BOOLEAN NOT NULL DEFAULT TRUE,
    receber_lembrete_treino BOOLEAN NOT NULL DEFAULT TRUE,
    receber_relatorio_progresso BOOLEAN NOT NULL DEFAULT TRUE,
    horario_preferencial TIME NOT NULL DEFAULT 00:51:21.014581,
    dias_antecedencia_pagamento INTEGER NOT NULL DEFAULT 3,
    email_alternativo VARCHAR(254) NOT NULL,
    telefone_alternativo VARCHAR(20) NOT NULL
);


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
