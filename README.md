# FormaFit - Sistema para Personal Trainers

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0-blue)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Um sistema web completo desenvolvido em Django para personal trainers gerenciarem seus alunos, treinos, frequência e finanças de forma eficiente e profissional.

## 📋 Funcionalidades

### 🏋️‍♂️ Gerenciamento de Alunos
- Cadastro completo com dados pessoais e físicos
- Histórico de medidas corporais e evolução
- Fotos de progresso com galeria organizada
- Objetivos e observações personalizadas
- Controle de status ativo/inativo

### 💪 Planos de Treino
- Criação de treinos organizados por dias da semana
- Catálogo completo de exercícios por grupo muscular
- Especificações detalhadas (séries, repetições, carga, descanso)
- Cópia e personalização de planos existentes
- Ativação/desativação de planos por aluno

### 📊 Controle de Frequência
- Registro de presença nas aulas
- Agendamento de treinos futuros
- Relatórios de frequência mensal
- Histórico completo de participação

### 💰 Gestão Financeira
- Contratos e planos de mensalidade
- Geração automática de faturas
- Controle de pagamentos e inadimplência
- Relatórios financeiros detalhados

### 📈 Relatórios de Evolução
- Relatórios automáticos de progresso
- Gráficos de evolução de peso e medidas
- Exportação em PDF profissional
- Compartilhamento com alunos

### 🔔 Notificações Automáticas
- Lembretes de pagamento via WhatsApp
- Notificações de treino por email
- Configurações personalizáveis de envio
- Integração com API ChatPro

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.9+** - Linguagem principal
- **Django 4.2** - Framework web
- **PostgreSQL** - Banco de dados (produção)
- **SQLite** - Banco de dados (desenvolvimento)

### Frontend
- **HTML5 & CSS3** - Estrutura e estilização
- **JavaScript** - Interatividade
- **Tailwind CSS** - Framework CSS utilitário
- **Templates Django** - Sistema de templates

### Integrações
- **API ChatPro** - Envio de WhatsApp
- **Pillow** - Processamento de imagens
- **Python-decouple** - Gerenciamento de configurações
- **Django CORS** - Controle de CORS

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/formafit.git
cd formafit
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# No macOS/Linux
source venv/bin/activate

# No Windows
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
# Configurações básicas
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de dados PostgreSQL (produção)
# DATABASE_URL=postgresql://usuario:senha@localhost:5432/formafit

# Configurações de email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app

# API WhatsApp ChatPro
CHATPRO_API_TOKEN=seu-token-chatpro
CHATPRO_INSTANCE_ID=sua-instancia

# Configurações de mídia
MEDIA_ROOT=media/
STATIC_ROOT=staticfiles/
```

### 5. Execute as migrações
```bash
python manage.py migrate
```

### 6. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 7. Execute o servidor de desenvolvimento
```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000` no seu navegador.

## 🏗️ Estrutura do Projeto

```
formafit/
├── formafit/                 # Configurações principais do Django
│   ├── settings.py          # Configurações do projeto
│   ├── urls.py              # URLs principais
│   └── wsgi.py              # WSGI para produção
├── accounts/                # Autenticação e usuários
│   ├── models.py            # Modelo de usuário customizado
│   ├── views.py             # Views de autenticação
│   └── forms.py             # Formulários de usuário
├── alunos/                  # Gerenciamento de alunos
│   ├── models.py            # Modelos de aluno, medidas, fotos
│   ├── views.py             # Views CRUD e relatórios
│   └── forms.py             # Formulários de aluno
├── treinos/                 # Planos de treino e exercícios
│   ├── models.py            # Modelos de treino e exercícios
│   ├── views.py             # Views de criação e gestão
│   └── forms.py             # Formulários de treino
├── frequencia/              # Controle de presença
│   ├── models.py            # Modelos de frequência
│   └── views.py             # Registro de presença
├── financeiro/              # Gestão financeira
│   ├── models.py            # Modelos de fatura e pagamento
│   └── views.py             # Controle financeiro
├── relatorios/              # Geração de relatórios
│   ├── models.py            # Modelos de relatório
│   └── views.py             # Geração de PDFs
├── notificacoes/            # Sistema de notificações
│   ├── models.py            # Modelos de notificação
│   └── views.py             # Envio de mensagens
├── templates/               # Templates HTML
│   ├── base.html            # Template base
│   ├── accounts/            # Templates de autenticação
│   ├── alunos/              # Templates de alunos
│   └── ...                  # Outros templates
├── static/                  # Arquivos estáticos (CSS, JS, imagens)
├── media/                   # Arquivos de mídia (uploads)
├── requirements.txt         # Dependências Python
└── manage.py               # Utilitário de linha de comando do Django
```

## 🎨 Interface do Usuário

O FormaFit possui uma interface moderna e responsiva, desenvolvida com Tailwind CSS:

- **Design responsivo** que funciona em desktop, tablet e mobile
- **Navegação lateral** com acesso rápido a todas as funcionalidades
- **Dashboard intuitivo** com estatísticas e ações rápidas
- **Formulários limpos** com validação em tempo real
- **Tabelas organizadas** com filtros e paginação
- **Modais e componentes** interativos para melhor UX

## 📱 Funcionalidades Principais

### Dashboard
- Visão geral de alunos, treinos e finanças
- Agenda do dia com próximos treinos
- Ações rápidas para tarefas comuns
- Estatísticas de desempenho

### Gerenciamento de Alunos
- Lista completa com filtros avançados
- Fichas detalhadas com histórico completo
- Acompanhamento de evolução física
- Galeria de fotos de progresso

### Criação de Treinos
- Interface intuitiva para montar treinos
- Biblioteca de exercícios organizada
- Especificações técnicas detalhadas
- Sistema de cópia e personalização

### Controle Financeiro
- Dashboard financeiro com gráficos
- Geração automática de faturas
- Controle de inadimplência
- Relatórios de receita

## 🔧 Desenvolvimento

### Executar em modo de desenvolvimento
```bash
python manage.py runserver
```

### Executar testes
```bash
python manage.py test
```

### Criar novas migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### Coletar arquivos estáticos (produção)
```bash
python manage.py collectstatic
```

## 🚀 Deploy em Produção

### Configurações necessárias:
1. Configure PostgreSQL como banco de dados
2. Configure servidor web (Nginx + Gunicorn)
3. Configure SSL/HTTPS
4. Configure backup automático
5. Configure monitoramento

### Variáveis de ambiente para produção:
```env
DEBUG=False
ALLOWED_HOSTS=seudominio.com
DATABASE_URL=postgresql://...
SECRET_KEY=chave-super-secreta
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Perfil](https://linkedin.com/in/seu-perfil)
- Email: seu.email@exemplo.com

## 🙏 Agradecimentos

- Comunidade Django pela excelente documentação
- Tailwind CSS pela facilidade de estilização
- Todos os contribuidores que ajudaram no desenvolvimento

---

**FormaFit** - Transformando a gestão de personal trainers através da tecnologia! 💪
