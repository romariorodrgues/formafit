# FormaFit - Sistema Completo para Personal Trainers

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0-blue)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Um sistema web completo e moderno desenvolvido em Django para personal trainers gerenciarem seus alunos, treinos, frequência e finanças de forma eficiente e profissional. Interface responsiva e intuitiva com design moderno.

## 🎯 Visão Geral

O FormaFit foi desenvolvido para resolver os principais desafios dos personal trainers no dia a dia:
- **Organização**: Centralize todos os dados dos alunos em um só lugar
- **Eficiência**: Automatize tarefas repetitivas como geração de faturas
- **Profissionalismo**: Relatórios e comunicação profissional com os alunos
- **Controle Financeiro**: Gestão completa de mensalidades e inadimplência
- **Evolução**: Acompanhamento detalhado do progresso dos alunos

## ✨ Funcionalidades Principais

### 🏋️‍♂️ **Gerenciamento Completo de Alunos**
- ✅ Cadastro completo com dados pessoais, físicos e de contato
- ✅ Histórico detalhado de medidas corporais e evolução
- ✅ Galeria de fotos de progresso organizada por data
- ✅ Objetivos personalizados e observações importantes
- ✅ Controle de status ativo/inativo com histórico
- ✅ Busca e filtros avançados

### 💪 **Sistema de Treinos Avançado**
- ✅ Criação de planos de treino por dias da semana
- ✅ Catálogo completo de exercícios por grupo muscular
- ✅ Especificações detalhadas (séries, repetições, carga, descanso)
- ✅ Sistema de cópia e personalização de treinos
- ✅ Ativação/desativação de planos por aluno
- ✅ Histórico de treinos executados

### 📊 **Controle de Frequência e Agendamentos**
- ✅ Registro de presença nas aulas com horários
- ✅ Sistema de agendamento de treinos futuros
- ✅ Relatórios de frequência mensal e semanal
- ✅ Dashboard com visão geral de presença
- ✅ Histórico completo de participação

### 💰 **Gestão Financeira Completa**
- ✅ **Contratos e Planos**: Criação e gestão de contratos de mensalidade
- ✅ **Faturas Automáticas**: Geração automática de faturas mensais
- ✅ **Controle de Pagamentos**: Registro e acompanhamento de pagamentos
- ✅ **Inadimplência**: Dashboard específico para controle de atrasos
- ✅ **Relatórios Financeiros**: Métricas detalhadas de receita e performance
- ✅ **Filtros Avançados**: Busca por período, status, valor e aluno
- ✅ **Dashboard Executivo**: Visão geral das finanças em tempo real

### 📈 **Relatórios e Análises**
- ✅ Relatórios automáticos de progresso dos alunos
- ✅ Gráficos de evolução de peso e medidas corporais
- ✅ Exportação profissional em PDF
- ✅ Relatórios de frequência e performance
- ✅ Análises financeiras com métricas de negócio

### 🔔 **Sistema de Notificações**
- ✅ Configurações personalizáveis de notificações
- ✅ Lembretes de pagamento via WhatsApp (API ChatPro)
- ✅ Notificações de treino por email
- ✅ Alertas de vencimento de faturas
- ✅ Sistema de templates personalizáveis

### 🎨 **Interface e Experiência**
- ✅ Design moderno e responsivo com Tailwind CSS
- ✅ Dashboard intuitivo com métricas em tempo real
- ✅ Navegação fluida e experiência otimizada
- ✅ Filtros avançados em todas as listagens
- ✅ Paginação inteligente para grandes volumes de dados
- ✅ Breadcrumbs e navegação contextual

## �️ Tecnologias e Arquitetura

### **Backend**
- **Python 3.9+** - Linguagem principal
- **Django 4.2** - Framework web robusto e escalável
- **PostgreSQL** - Banco de dados (produção)
- **SQLite** - Banco de dados (desenvolvimento)
- **Django Rest Framework** - APIs RESTful (futuro)

### **Frontend**
- **HTML5 & CSS3** - Estrutura e estilização semântica
- **JavaScript ES6+** - Interatividade e dinamismo
- **Tailwind CSS** - Framework CSS utilitário e responsivo
- **Django Templates** - Sistema de templates robusto

### **Integrações e APIs**
- **API ChatPro** - Envio de mensagens WhatsApp
- **Pillow** - Processamento e otimização de imagens
- **Python-decouple** - Gerenciamento seguro de configurações
- **Django CORS** - Controle de Cross-Origin Resource Sharing

### **Ferramentas de Desenvolvimento**
- **Git** - Controle de versão
- **Virtual Environment** - Isolamento de dependências
- **Django Debug Toolbar** - Debugging avançado
- **pytest** - Testes automatizados (futuro)

## � Instalação e Configuração

### **Pré-requisitos**
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git
- PostgreSQL (para produção)

### **🛠️ Instalação Local (Desenvolvimento)**

#### **1. Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/FormaFit.git
cd FormaFit
```

#### **2. Crie e Ative o Ambiente Virtual**
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Linux/Mac
source venv/bin/activate

# Ativar no Windows
venv\Scripts\activate
```

#### **3. Instale as Dependências**
```bash
pip install -r requirements.txt
```

#### **4. Configure as Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
# Configurações Básicas
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de Dados (desenvolvimento com SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# API ChatPro (opcional para desenvolvimento)
CHATPRO_API_KEY=sua-chave-api-chatpro
CHATPRO_API_URL=https://api.chatpro.com.br

# Email (opcional para desenvolvimento)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

#### **5. Execute as Migrações**
```bash
python manage.py migrate
```

#### **6. Crie um Superusuário**
```bash
python manage.py createsuperuser
```

#### **7. Execute o Servidor de Desenvolvimento**
```bash
python manage.py runserver
```

Acesse: `http://localhost:8000`

### **🌐 Configuração para Produção**

#### **1. Servidor e Dependências**
```bash
# Instalar dependências do sistema (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx

# Instalar dependências do sistema (CentOS/RHEL)
sudo yum install python3 python3-pip postgresql postgresql-server nginx
```

#### **2. Configuração do PostgreSQL**
```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Criar banco e usuário
CREATE DATABASE formafit_db;
CREATE USER formafit_user WITH PASSWORD 'senha_segura_aqui';
ALTER ROLE formafit_user SET client_encoding TO 'utf8';
ALTER ROLE formafit_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE formafit_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE formafit_db TO formafit_user;
\q
```

#### **3. Clone e Configure o Projeto**
```bash
# Clone para diretório de produção
cd /var/www
sudo git clone https://github.com/seu-usuario/FormaFit.git
sudo chown -R www-data:www-data FormaFit
cd FormaFit

# Crie ambiente virtual
sudo -u www-data python3 -m venv venv
sudo -u www-data venv/bin/pip install -r requirements.txt
```

#### **4. Configuração de Produção (.env)**
```env
# Configurações de Produção
SECRET_KEY=chave-super-secreta-de-producao-256-bits
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# Banco PostgreSQL
DATABASE_URL=postgresql://formafit_user:senha_segura_aqui@localhost:5432/formafit_db

# APIs de Produção
CHATPRO_API_KEY=sua-chave-api-chatpro-producao
CHATPRO_API_URL=https://api.chatpro.com.br

# Email SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app

# Configurações de Segurança
SECURE_SSL_REDIRECT=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

#### **5. Migrações e Arquivos Estáticos**
```bash
# Executar migrações
sudo -u www-data venv/bin/python manage.py migrate

# Coletar arquivos estáticos
sudo -u www-data venv/bin/python manage.py collectstatic --noinput

# Criar superusuário
sudo -u www-data venv/bin/python manage.py createsuperuser
```

#### **6. Configuração do Gunicorn**
Crie `/etc/systemd/system/formafit.service`:
```ini
[Unit]
Description=FormaFit Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/FormaFit
Environment="PATH=/var/www/FormaFit/venv/bin"
ExecStart=/var/www/FormaFit/venv/bin/gunicorn --workers 3 --bind unix:/var/www/FormaFit/formafit.sock formafit.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar e iniciar serviço
sudo systemctl daemon-reload
sudo systemctl start formafit
sudo systemctl enable formafit
```

#### **7. Configuração do Nginx**
Crie `/etc/nginx/sites-available/formafit`:
```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/FormaFit;
    }
    
    location /media/ {
        root /var/www/FormaFit;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/FormaFit/formafit.sock;
    }
}
```

```bash
# Habilitar site
sudo ln -s /etc/nginx/sites-available/formafit /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### **8. SSL com Let's Encrypt (Opcional)**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

## 📁 Estrutura do Projeto
```
FormaFit/
├── 📁 accounts/                 # Autenticação e usuários
│   ├── migrations/
│   ├── models.py               # Modelo de usuário customizado
│   ├── views.py                # Views de auth e dashboard
│   ├── forms.py                # Formulários de registro/login
│   └── urls.py                 # URLs de autenticação
├── 📁 alunos/                  # Gestão de alunos
│   ├── migrations/
│   ├── models.py               # Modelo de aluno e medidas
│   ├── views.py                # CRUD de alunos
│   ├── forms.py                # Formulários de aluno
│   └── urls.py                 # URLs de alunos
├── 📁 treinos/                 # Sistema de treinos
│   ├── migrations/
│   ├── models.py               # Modelos de plano e exercício
│   ├── views.py                # Gestão de treinos
│   └── urls.py                 # URLs de treinos
├── 📁 frequencia/              # Controle de frequência
│   ├── migrations/
│   ├── models.py               # Modelo de agenda e presença
│   ├── views.py                # Controle de presença
│   └── urls.py                 # URLs de frequência
├── 📁 financeiro/              # Gestão financeira
│   ├── migrations/
│   ├── models.py               # Contratos, faturas, planos
│   ├── views.py                # Dashboard e gestão financeira
│   ├── forms.py                # Formulários financeiros
│   ├── services.py             # Serviços de negócio
│   └── urls.py                 # URLs financeiras
├── 📁 relatorios/              # Sistema de relatórios
│   ├── migrations/
│   ├── models.py               # Configurações de relatório
│   ├── views.py                # Geração de relatórios
│   ├── services.py             # Serviços de PDF
│   └── management/commands/    # Comandos customizados
├── 📁 notificacoes/            # Sistema de notificações
│   ├── migrations/
│   ├── models.py               # Configurações e logs
│   ├── views.py                # Gestão de notificações
│   └── urls.py                 # URLs de notificações
├── 📁 templates/               # Templates HTML
│   ├── base.html               # Template base
│   ├── 📁 accounts/            # Templates de autenticação
│   ├── 📁 alunos/              # Templates de alunos
│   ├── 📁 financeiro/          # Templates financeiros
│   └── ...
├── 📁 static/                  # Arquivos estáticos
├── 📁 media/                   # Uploads de usuário
├── 📁 formafit/                # Configurações Django
│   ├── settings.py             # Configurações principais
│   ├── urls.py                 # URLs principais
│   └── wsgi.py                 # WSGI para produção
├── 📄 manage.py                # Comando Django
├── 📄 requirements.txt         # Dependências Python
├── 📄 .env.example             # Exemplo de configuração
└── 📄 README.md                # Este arquivo
```

## 🎯 Módulos e Funcionalidades Detalhadas

### **🏋️‍♂️ Módulo de Alunos**
- **Cadastro Completo**: Dados pessoais, físicos, contato e objetivos
- **Medidas Corporais**: Histórico de peso, altura, % de gordura, etc.
- **Fotos de Progresso**: Upload e organização de fotos por data
- **Gestão de Status**: Controle de alunos ativos/inativos
- **Busca Avançada**: Filtros por nome, status, data de cadastro

### **💪 Módulo de Treinos**
- **Planos Personalizados**: Criação por dias da semana
- **Catálogo de Exercícios**: Organizados por grupo muscular
- **Especificações Técnicas**: Séries, repetições, carga, descanso
- **Cópia de Planos**: Reutilização e personalização
- **Histórico de Execução**: Acompanhamento de progresso

### **📊 Módulo de Frequência**
- **Registro de Presença**: Check-in/check-out com horários
- **Agendamento**: Sistema de reserva de horários
- **Relatórios de Frequência**: Análises mensais e semanais
- **Dashboard de Presença**: Visão geral em tempo real

### **💰 Módulo Financeiro (Completo)**
- **Dashboard Executivo**: Métricas financeiras em tempo real
- **Gestão de Contratos**: Criação e acompanhamento de contratos
- **Planos de Mensalidade**: Definição de valores e condições
- **Faturas Automáticas**: Geração automática baseada nos contratos
- **Controle de Pagamentos**: Registro e acompanhamento
- **Inadimplência**: Dashboard específico para controle de atrasos
- **Relatórios Financeiros**: Análises de receita e performance
- **Filtros Avançados**: Busca por múltiplos critérios

### **📈 Módulo de Relatórios**
- **Relatórios de Progresso**: PDF profissional para alunos
- **Gráficos de Evolução**: Visualização de medidas e peso
- **Relatórios de Frequência**: Análise de presença
- **Relatórios Financeiros**: Métricas de negócio
- **Exportação**: PDF otimizado para impressão

### **🔔 Módulo de Notificações**
- **WhatsApp**: Integração com API ChatPro
- **Email**: Notificações automáticas por email
- **Configurações**: Personalização de horários e tipos
- **Templates**: Mensagens personalizáveis
- **Logs**: Histórico de envios

## 🔧 Comandos Úteis

### **Desenvolvimento**
```bash
# Executar servidor de desenvolvimento
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell interativo
python manage.py shell
```

### **Manutenção**
```bash
# Backup do banco de dados
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json

# Limpar sessões expiradas
python manage.py clearsessions

# Verificar configurações
python manage.py check
```

## 🚀 Deploy e Monitoramento

### **Checklist de Deploy**
- [ ] Configurar variáveis de ambiente de produção
- [ ] Configurar banco PostgreSQL
- [ ] Executar migrações
- [ ] Coletar arquivos estáticos
- [ ] Configurar servidor web (Nginx)
- [ ] Configurar SSL/HTTPS
- [ ] Configurar backups automáticos
- [ ] Configurar monitoramento

### **Monitoramento**
```bash
# Status do serviço
sudo systemctl status formafit

# Logs do aplicação
sudo journalctl -u formafit -f

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitorar recursos
htop
df -h
```

## 📊 Performance e Otimizações

### **Otimizações Implementadas**
- ✅ **Queries Otimizadas**: select_related e prefetch_related
- ✅ **Paginação**: Listagens paginadas para performance
- ✅ **Índices de Banco**: Campos frequentemente consultados
- ✅ **Cache de Template**: Templates compilados
- ✅ **Compressão de Imagens**: Otimização automática
- ✅ **Lazy Loading**: Carregamento sob demanda

### **Métricas Recomendadas**
- Tempo de resposta < 200ms (páginas simples)
- Tempo de resposta < 500ms (páginas com gráficos)
- Uso de memória < 512MB por worker
- Tempo de query < 100ms (95% das queries)

## 🛡️ Segurança

### **Implementações de Segurança**
- ✅ **Autenticação Robusta**: Sistema de login seguro
- ✅ **Autorização**: Controle de acesso por usuário
- ✅ **CSRF Protection**: Proteção contra ataques CSRF
- ✅ **SQL Injection**: Prevenção via ORM Django
- ✅ **XSS Protection**: Sanitização de inputs
- ✅ **HTTPS**: Configuração de SSL/TLS
- ✅ **Headers de Segurança**: Configurações adequadas

### **Boas Práticas de Segurança**
- Use senhas fortes para banco de dados
- Mantenha SECRET_KEY segura e única
- Configure ALLOWED_HOSTS adequadamente
- Use HTTPS em produção
- Mantenha dependências atualizadas
- Configure backups regulares

## 🤝 Contribuindo

### **Como Contribuir**
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### **Padrões de Desenvolvimento**
- Siga PEP 8 para código Python
- Use nomes descritivos em português para models e views
- Documente funções e classes importantes
- Escreva testes para novas funcionalidades
- Mantenha templates responsivos

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte e Contato

- **Documentação**: [Wiki do Projeto](https://github.com/seu-usuario/FormaFit/wiki)
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/FormaFit/issues)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/FormaFit/discussions)

## 🎉 Agradecimentos

- Comunidade Django pela excelente documentação
- Tailwind CSS pelo framework CSS intuitivo
- ChatPro pela API de WhatsApp
- Todos os personal trainers que contribuíram com feedback

---

**FormaFit** - Transformando a gestão de personal trainers através da tecnologia! 🏋️‍♂️💪

*Desenvolvido com ❤️ para a comunidade fitness*
