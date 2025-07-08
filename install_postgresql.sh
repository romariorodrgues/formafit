#!/bin/bash

# =================================================================
# FORMAFIT - SCRIPT DE INSTALAÇÃO POSTGRESQL
# =================================================================
# Script automatizado para configurar PostgreSQL para o FormaFit
# Compatível com macOS e Linux
# =================================================================

set -e  # Para na primeira falha

echo "🚀 FormaFit - Instalação PostgreSQL"
echo "==================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir com cor
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Detectar sistema operacional
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    else
        print_error "Sistema operacional não suportado: $OSTYPE"
        exit 1
    fi
    print_info "Sistema detectado: $OS"
}

# Verificar se PostgreSQL está instalado
check_postgresql() {
    if command -v psql &> /dev/null; then
        print_status "PostgreSQL encontrado"
        PSQL_VERSION=$(psql --version | awk '{print $3}')
        print_info "Versão: $PSQL_VERSION"
        return 0
    else
        print_warning "PostgreSQL não encontrado"
        return 1
    fi
}

# Instalar PostgreSQL
install_postgresql() {
    print_info "Instalando PostgreSQL..."
    
    if [[ "$OS" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            brew install postgresql
            brew services start postgresql
        else
            print_error "Homebrew não encontrado. Instale manualmente o PostgreSQL"
            print_info "Visite: https://postgresapp.com/"
            exit 1
        fi
    elif [[ "$OS" == "linux" ]]; then
        # Ubuntu/Debian
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y postgresql postgresql-contrib
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
        # CentOS/RHEL
        elif command -v yum &> /dev/null; then
            sudo yum install -y postgresql-server postgresql-contrib
            sudo postgresql-setup initdb
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
        else
            print_error "Gerenciador de pacotes não suportado"
            exit 1
        fi
    fi
    
    print_status "PostgreSQL instalado com sucesso"
}

# Configurar banco de dados
setup_database() {
    print_info "Configurando banco de dados FormaFit..."
    
    # Verificar se o usuário postgres existe
    if [[ "$OS" == "macos" ]]; then
        # No macOS com Homebrew, o usuário padrão é o usuário atual
        DB_USER=$(whoami)
        PSQL_CMD="psql postgres"
    else
        # No Linux, usar o usuário postgres
        DB_USER="postgres"
        PSQL_CMD="sudo -u postgres psql"
    fi
    
    # Executar script de configuração
    print_info "Criando usuário e banco de dados..."
    
    $PSQL_CMD << EOF
-- Criar usuário se não existir
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'formafit_user') THEN
        CREATE USER formafit_user WITH PASSWORD 'formafit123';
    END IF;
END
\$\$;

-- Criar banco se não existir
SELECT 'CREATE DATABASE formafit_db OWNER formafit_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'formafit_db')\gexec

-- Dar privilégios
GRANT ALL PRIVILEGES ON DATABASE formafit_db TO formafit_user;
ALTER USER formafit_user CREATEDB;
EOF

    # Configurar permissões no banco
    $PSQL_CMD -d formafit_db << EOF
GRANT ALL ON SCHEMA public TO formafit_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO formafit_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO formafit_user;
EOF

    print_status "Banco de dados configurado"
}

# Verificar dependências Python
check_python_deps() {
    print_info "Verificando dependências Python..."
    
    if python -c "import psycopg2" 2>/dev/null; then
        print_status "psycopg2 encontrado"
    else
        print_warning "psycopg2 não encontrado, instalando..."
        pip install psycopg2-binary
        print_status "psycopg2 instalado"
    fi
}

# Criar arquivo .env se não existir
setup_env_file() {
    if [[ ! -f ".env" ]]; then
        print_info "Criando arquivo .env..."
        cp .env.example .env
        
        # Gerar SECRET_KEY aleatória
        SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
        
        # Atualizar .env com configurações
        sed -i.bak "s/your-secret-key-here-make-it-very-long-and-secure/$SECRET_KEY/" .env
        
        print_status "Arquivo .env criado"
    else
        print_warning "Arquivo .env já existe"
    fi
}

# Executar migrações Django
run_migrations() {
    print_info "Executando migrações Django..."
    
    python manage.py migrate
    
    print_status "Migrações executadas"
}

# Função principal
main() {
    echo
    print_info "Iniciando instalação..."
    
    # Verificar se estamos no diretório correto
    if [[ ! -f "manage.py" ]]; then
        print_error "Execute este script no diretório raiz do projeto FormaFit"
        exit 1
    fi
    
    # Detectar sistema operacional
    detect_os
    
    # Verificar/instalar PostgreSQL
    if ! check_postgresql; then
        read -p "PostgreSQL não encontrado. Deseja instalar? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_postgresql
        else
            print_error "PostgreSQL é necessário para continuar"
            exit 1
        fi
    fi
    
    # Configurar banco de dados
    setup_database
    
    # Verificar dependências Python
    check_python_deps
    
    # Configurar arquivo .env
    setup_env_file
    
    # Executar migrações
    run_migrations
    
    # Sucesso!
    echo
    print_status "Instalação concluída com sucesso!"
    echo
    print_info "Próximos passos:"
    echo "1. Crie um superusuário: python manage.py createsuperuser"
    echo "2. Execute o servidor: python manage.py runserver"
    echo "3. Acesse: http://localhost:8000"
    echo
    print_info "Credenciais do banco:"
    echo "   Database: formafit_db"
    echo "   User: formafit_user"
    echo "   Password: formafit123"
    echo "   Host: localhost"
    echo "   Port: 5432"
}

# Executar script principal
main "$@"
