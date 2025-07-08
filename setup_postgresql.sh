#!/bin/bash

# =====================================================
# FORMAFIT - SCRIPT DE INSTALAÇÃO POSTGRESQL
# =====================================================
# 
# Este script automatiza a instalação do PostgreSQL
# e configuração do banco de dados FormaFit
#
# =====================================================

set -e  # Parar em caso de erro

echo "======================================================="
echo "FORMAFIT - CONFIGURAÇÃO POSTGRESQL"
echo "======================================================="
echo ""

# Verificar se PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL não encontrado!"
    echo ""
    echo "Instale o PostgreSQL primeiro:"
    echo "  macOS: brew install postgresql"
    echo "  Ubuntu: sudo apt install postgresql postgresql-contrib"
    echo "  CentOS: sudo yum install postgresql postgresql-server"
    echo ""
    exit 1
fi

echo "✅ PostgreSQL encontrado"

# Verificar se o serviço está rodando
if ! pg_isready -q; then
    echo "⚠️  Iniciando serviço PostgreSQL..."
    
    # Tentar iniciar o serviço baseado no sistema
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew services start postgresql || true
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo systemctl start postgresql || sudo service postgresql start || true
    fi
    
    sleep 2
    
    if ! pg_isready -q; then
        echo "❌ Não foi possível iniciar o PostgreSQL"
        echo "Inicie o serviço manualmente e execute este script novamente"
        exit 1
    fi
fi

echo "✅ PostgreSQL está rodando"

# Configurações do banco
DB_NAME="formafit_db"
DB_USER="formafit_user"
DB_PASSWORD="formafit123"

echo ""
echo "Configurações do banco:"
echo "  Nome: $DB_NAME"
echo "  Usuário: $DB_USER"
echo "  Senha: $DB_PASSWORD"
echo ""

# Função para executar comandos SQL como postgres
run_sql_as_postgres() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        psql -d postgres -c "$1"
    else
        # Linux
        sudo -u postgres psql -c "$1"
    fi
}

# Criar banco de dados
echo "🔧 Criando banco de dados..."
run_sql_as_postgres "DROP DATABASE IF EXISTS $DB_NAME;" || true
run_sql_as_postgres "CREATE DATABASE $DB_NAME;"

# Criar usuário
echo "🔧 Criando usuário..."
run_sql_as_postgres "DROP USER IF EXISTS $DB_USER;" || true
run_sql_as_postgres "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"

# Conceder permissões
echo "🔧 Configurando permissões..."
run_sql_as_postgres "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
run_sql_as_postgres "ALTER USER $DB_USER CREATEDB;"

# Importar estrutura
if [ -f "database_schema.sql" ]; then
    echo "🔧 Importando estrutura do banco..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        psql -U $DB_USER -d $DB_NAME -f database_schema.sql
    else
        sudo -u postgres psql -U $DB_USER -d $DB_NAME -f database_schema.sql
    fi
    echo "✅ Estrutura importada com sucesso"
else
    echo "⚠️  Arquivo database_schema.sql não encontrado"
    echo "Execute: python generate_postgresql_schema.py"
fi

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "🔧 Criando arquivo .env..."
    cp .env.example .env
    
    # Atualizar configurações do banco no .env
    sed -i.bak "s/DATABASE_NAME=.*/DATABASE_NAME=$DB_NAME/" .env
    sed -i.bak "s/DATABASE_USER=.*/DATABASE_USER=$DB_USER/" .env
    sed -i.bak "s/DATABASE_PASSWORD=.*/DATABASE_PASSWORD=$DB_PASSWORD/" .env
    sed -i.bak "s/DATABASE_HOST=.*/DATABASE_HOST=localhost/" .env
    sed -i.bak "s/DATABASE_PORT=.*/DATABASE_PORT=5432/" .env
    
    # Remover linha USE_SQLITE se existir
    sed -i.bak '/USE_SQLITE/d' .env
    
    rm .env.bak 2>/dev/null || true
    
    echo "✅ Arquivo .env criado e configurado"
else
    echo "ℹ️  Arquivo .env já existe"
fi

# Instalar dependências Python se necessário
if [ -f "requirements.txt" ]; then
    echo "🔧 Verificando dependências Python..."
    
    # Verificar se psycopg2 está instalado
    python -c "import psycopg2" 2>/dev/null || {
        echo "📦 Instalando psycopg2-binary..."
        pip install psycopg2-binary
    }
    
    echo "✅ Dependências verificadas"
fi

echo ""
echo "======================================================="
echo "✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!"
echo "======================================================="
echo ""
echo "Próximos passos:"
echo ""
echo "1. Aplicar migrações:"
echo "   python manage.py migrate --fake-initial"
echo ""
echo "2. Criar superusuário:"
echo "   python manage.py createsuperuser"
echo ""
echo "3. Executar scripts de dados iniciais:"
echo "   python criar_dados_notificacoes.py"
echo "   python criar_notificacoes_exemplo.py"
echo ""
echo "4. Iniciar servidor:"
echo "   python manage.py runserver"
echo ""
echo "Dados de acesso:"
echo "  Banco: $DB_NAME"
echo "  Usuário: $DB_USER"
echo "  Senha: $DB_PASSWORD"
echo "  Host: localhost"
echo "  Porta: 5432"
echo ""
echo "🎉 Pronto para usar o FormaFit!"
echo "======================================================="
