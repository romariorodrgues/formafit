<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# FormaFit - Sistema para Personal Trainers

Este é um sistema completo desenvolvido em Django para personal trainers gerenciarem seus alunos, treinos, frequência e finanças.

## Tecnologias Utilizadas
- **Backend**: Python, Django 4.2
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS  
- **Banco de Dados**: PostgreSQL
- **Integrações**: API ChatPro para WhatsApp

## Estrutura do Projeto

### Apps Django:
- **accounts**: Autenticação e usuários (personal trainers)
- **alunos**: Gerenciamento de alunos e medidas corporais
- **treinos**: Planos de treino e exercícios
- **frequencia**: Controle de presença e agendamentos
- **financeiro**: Gestão de mensalidades e pagamentos
- **notificacoes**: Sistema de notificações automáticas
- **relatorios**: Geração de relatórios de progresso em PDF

## Funcionalidades Principais

1. **Gerenciamento de Alunos**
   - Cadastro completo com dados pessoais e físicos
   - Histórico de medidas corporais e fotos de progresso
   - Objetivos e observações personalizadas

2. **Planos de Treino**
   - Criação de treinos organizados por dias da semana
   - Catálogo de exercícios por grupo muscular
   - Especificações detalhadas (séries, repetições, carga)

3. **Controle de Frequência**
   - Registro de presença nas aulas
   - Agendamento de treinos futuros
   - Relatórios de frequência mensal

4. **Gestão Financeira**
   - Contratos e planos de mensalidade
   - Geração automática de faturas
   - Controle de pagamentos e inadimplência

5. **Relatórios de Evolução**
   - Relatórios automáticos de progresso
   - Gráficos de evolução de peso e medidas
   - Exportação em PDF

6. **Notificações Automáticas**
   - Lembretes de pagamento via WhatsApp
   - Notificações de treino
   - E-mails automáticos com relatórios

## Padrões de Código

- Use nomes em português para modelos, campos e variáveis quando apropriado
- Documente todas as classes e métodos importantes
- Siga as convenções do Django para estrutura de projetos
- Use Tailwind CSS para estilização responsiva
- Implemente validações adequadas nos formulários
- Mantenha a segurança em mente (autenticação, autorização)

## Configurações Importantes

- O modelo de usuário customizado está em `accounts.User`
- Configurações de banco PostgreSQL estão no `.env`
- API ChatPro configurada para envio de WhatsApp
- Templates organizados na pasta `templates/`
- Arquivos estáticos em `static/` com Tailwind CSS

## Instalação e Configuração

1. Ativar ambiente virtual: `source venv/bin/activate`
2. Instalar dependências: `pip install -r requirements.txt`
3. Configurar variáveis no `.env`
4. Executar migrações: `python manage.py migrate`
5. Criar superusuário: `python manage.py createsuperuser`
6. Executar servidor: `python manage.py runserver`

## Objetivo do Sistema

O FormaFit visa facilitar a gestão completa de personal trainers, proporcionando:
- Maior organização no atendimento aos alunos
- Controle eficiente de frequência e evolução
- Gestão financeira automatizada
- Comunicação eficaz através de notificações
- Relatórios profissionais de progresso

Este sistema permite que personal trainers foquem no que fazem de melhor: treinar e motivar seus alunos, enquanto a tecnologia cuida da parte administrativa.
