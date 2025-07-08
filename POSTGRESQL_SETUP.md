# PostgreSQL - Configuração para Desenvolvimento

Este documento explica como configurar o PostgreSQL para desenvolvimento local do FormaFit.

## 🎯 **Objetivo**

Usar PostgreSQL tanto para desenvolvimento quanto para produção, garantindo compatibilidade total e evitando problemas de migração de SQLite para PostgreSQL.

## 📋 **Pré-requisitos**

- PostgreSQL 12+ instalado
- Python 3.9+
- psycopg2-binary (incluído no requirements.txt)

## 🚀 **Instalação Rápida (Automatizada)**

```bash
# Executar script de instalação automatizada
./install_postgresql.sh
```

Este script vai:
- ✅ Detectar seu sistema operacional
- ✅ Instalar PostgreSQL se necessário
- ✅ Criar usuário e banco de dados
- ✅ Configurar permissões
- ✅ Instalar dependências Python
- ✅ Criar arquivo .env
- ✅ Executar migrações Django

## 🔧 **Instalação Manual**

### 1. **Instalar PostgreSQL**

#### **macOS (Homebrew)**
```bash
brew install postgresql
brew services start postgresql
```

#### **Ubuntu/Debian**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### **CentOS/RHEL**
```bash
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. **Configurar Banco de Dados**

```bash
# Executar script SQL de configuração
psql -U postgres -f postgresql_setup.sql
```

Ou manualmente:

```sql
-- Conectar ao PostgreSQL como superuser
psql -U postgres

-- Criar usuário
CREATE USER formafit_user WITH PASSWORD 'formafit123';

-- Criar banco
CREATE DATABASE formafit_db OWNER formafit_user;

-- Dar privilégios
GRANT ALL PRIVILEGES ON DATABASE formafit_db TO formafit_user;
ALTER USER formafit_user CREATEDB;

-- Conectar ao banco
\c formafit_db;

-- Configurar permissões
GRANT ALL ON SCHEMA public TO formafit_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO formafit_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO formafit_user;
```

### 3. **Configurar Ambiente**

Copie `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

Edite o `.env`:
```bash
# Banco de dados
DATABASE_NAME=formafit_db
DATABASE_USER=formafit_user
DATABASE_PASSWORD=formafit123
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Não usar SQLite
# USE_SQLITE=False  # (comentado = padrão)
```

### 4. **Executar Migrações**

```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

## 📊 **Estrutura do Banco**

O sistema criará automaticamente as seguintes tabelas:

### **Autenticação e Usuários**
- `auth_*` - Tabelas padrão do Django
- `accounts_user` - Usuários personalizados (Personal Trainers)

### **Gestão de Alunos**
- `alunos_aluno` - Dados dos alunos
- `alunos_medidascorporais` - Histórico de medidas
- `alunos_fotoprogresso` - Fotos de evolução

### **Sistema de Treinos**
- `treinos_*` - Planos de treino e exercícios

### **Controle Financeiro**
- `financeiro_contrato` - Contratos de mensalidade
- `financeiro_plano` - Planos de pagamento
- `financeiro_fatura` - Faturas geradas
- `financeiro_pagamento` - Pagamentos recebidos

### **Notificações**
- `notificacoes_*` - Sistema de notificações WhatsApp/Email

### **Frequência e Relatórios**
- `frequencia_*` - Controle de presença
- `relatorios_*` - Configurações de relatórios

## 🔍 **Verificação da Instalação**

### **Verificar Conexão**
```bash
# Testar conexão com o banco
psql -U formafit_user -d formafit_db -h localhost

# Dentro do psql, listar tabelas
\dt
```

### **Verificar Django**
```bash
# Verificar configuração do banco
python manage.py dbshell

# Verificar se as migrações foram aplicadas
python manage.py showmigrations
```

## 🛠️ **Comandos Úteis**

### **Backup e Restore**
```bash
# Criar backup
pg_dump -U formafit_user -h localhost formafit_db > backup_formafit.sql

# Restaurar backup
psql -U formafit_user -h localhost formafit_db < backup_formafit.sql
```

### **Reset do Banco**
```bash
# Apagar e recriar banco (CUIDADO!)
dropdb -U postgres formafit_db
createdb -U postgres -O formafit_user formafit_db
python manage.py migrate
```

### **Monitoramento**
```bash
# Ver conexões ativas
psql -U postgres -c "SELECT * FROM pg_stat_activity WHERE datname = 'formafit_db';"

# Ver tamanho do banco
psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('formafit_db'));"
```

## 📈 **Performance**

### **Índices Importantes**
O sistema criará automaticamente índices para:
- Busca de alunos por nome
- Filtros de status ativo/inativo
- Consultas por data de vencimento
- Filtros de status de pagamento

### **Configurações Recomendadas**

Para desenvolvimento local, adicione ao `postgresql.conf`:
```
# Configurações para desenvolvimento
shared_preload_libraries = 'pg_stat_statements'
log_statement = 'all'
log_min_duration_statement = 100
```

## 🚨 **Troubleshooting**

### **Erro de Conexão**
```bash
# Verificar se PostgreSQL está rodando
brew services list | grep postgresql  # macOS
systemctl status postgresql           # Linux

# Verificar porta
netstat -an | grep 5432
```

### **Erro de Permissão**
```sql
-- Dar todas as permissões novamente
GRANT ALL PRIVILEGES ON DATABASE formafit_db TO formafit_user;
GRANT ALL ON SCHEMA public TO formafit_user;
```

### **Erro de Migração**
```bash
# Resetar migrações (CUIDADO!)
python manage.py migrate --fake-initial
```

## 🔄 **Instalação em Nova Máquina**

Para instalar o projeto em um novo computador:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/romariorodrgues/formafit.git
   cd FormaFit
   ```

2. **Execute a configuração automática:**
   ```bash
   ./install_postgresql.sh
   ```

3. **Finalize a instalação:**
   ```bash
   python manage.py createsuperuser
   python manage.py runserver
   ```

## 📁 **Arquivos Importantes**

- `postgresql_setup.sql` - Configuração rápida do banco
- `install_postgresql.sh` - Script de instalação automática
- `generate_postgresql_structure.py` - Gerador da estrutura SQL
- `.env.example` - Exemplo de configuração

## 🎯 **Vantagens do PostgreSQL**

1. **Consistência**: Mesmo banco em desenvolvimento e produção
2. **Performance**: Melhor para consultas complexas
3. **Recursos Avançados**: JSON, arrays, funções personalizadas
4. **Escalabilidade**: Preparado para crescimento
5. **Integridade**: Constraints e validações rigorosas

## 📝 **Próximos Passos**

Após configurar o PostgreSQL:

1. ✅ Execute o servidor: `python manage.py runserver`
2. ✅ Acesse: `http://localhost:8000`
3. ✅ Faça login com as credenciais de teste
4. ✅ Teste todas as funcionalidades
5. ✅ Configure notificações WhatsApp (opcional)

---

**O FormaFit agora está 100% preparado para PostgreSQL!** 🚀
