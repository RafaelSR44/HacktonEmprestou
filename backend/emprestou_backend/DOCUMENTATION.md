# Documentação da Aplicação Emprestou

Este documento detalha a arquitetura, funcionalidades e instruções para configurar e executar o backend da aplicação Emprestou.

## 1. Visão Geral da Aplicação

A aplicação Emprestou é uma plataforma de empréstimos peer-to-peer (P2P) que conecta mutuários (devedores) a credores. Ela gerencia todo o ciclo de vida do empréstimo, desde a solicitação e oferta até o matching, aceitação e pagamento das parcelas. As principais funcionalidades incluem:

*   **Autenticação e Gerenciamento de Usuários**: Registro e login de usuários via WhatsApp, com geração de tokens JWT para autenticação.
*   **KYC (Know Your Customer)**: Processo de verificação de identidade para usuários, incluindo validação de documentos e correspondência facial (atualmente utilizando serviços mock).
*   **Score de Crédito**: Avaliação do risco de crédito dos mutuários (atualmente utilizando um serviço mock).
*   **Gerenciamento de Empréstimos**: Criação de solicitações e ofertas de empréstimo, um sistema de matching para conectar mutuários e credores, e a aceitação de empréstimos que gera um contrato e um plano de parcelamento.
*   **Processamento de Pagamentos e Transações**: Gerenciamento do pagamento de parcelas, atualização de saldos de contas e registro detalhado de todas as transações financeiras.

## 2. Estrutura do Projeto (Backend)

O backend é construído com Flask e SQLAlchemy, seguindo uma estrutura modular:

```
emprestou_backend/
├── src/
│   ├── __init__.py             # Inicialização do Flask app, SQLAlchemy e JWT
│   ├── main.py                 # Ponto de entrada principal da aplicação
│   ├── config.py               # Configurações da aplicação (DB URI, JWT Secret, etc.)
│   ├── models/                 # Definições dos modelos de banco de dados (User, Loan, Transaction, etc.)
│   ├── routes/                 # Definição das rotas da API (Auth, Loans, KYC, Payments, etc.)
│   ├── services/               # Lógica de negócio e serviços (MatchingService, AuthService, PaymentService, etc.)
│   ├── mocks/                  # Serviços mock para integração externa (KYC, Score, Payment)
│   └── static/                 # Arquivos estáticos (se houver)
├── migrations/                 # Scripts de migração do Alembic
├── requirements.txt            # Dependências do Python
└── create_db.py                # Script auxiliar para criar o banco de dados (SQLite)
```

## 3. Configuração do Ambiente

### Pré-requisitos

*   Python 3.8+
*   pip (gerenciador de pacotes Python)
*   git
*   jq (para testar as APIs via cURL)

### Passos para Configuração

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/RafaelSR44/HacktonEmprestou.git
    cd HacktonEmprestou/backend/emprestou_backend
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuração do Banco de Dados (SQLite):**
    A aplicação utiliza SQLite por padrão. O arquivo `config.py` já está configurado para usar `app.db` no diretório raiz do `emprestou_backend`.

    Para criar o banco de dados e as tabelas, execute o script auxiliar:
    ```bash
    python3 create_db.py
    ```
    Este script garante que o banco de dados `app.db` seja criado e todas as tabelas definidas nos modelos sejam geradas.

## 4. Executando a Aplicação (Backend)

Para iniciar o servidor Flask:

1.  **Certifique-se de que o ambiente virtual está ativado.**
2.  **Defina a variável de ambiente `FLASK_APP` e execute o Flask:**
    ```bash
    export FLASK_APP=src/main.py
    flask run --host=0.0.0.0 --port=5000
    ```
    O servidor estará disponível em `http://0.0.0.0:5000`.

    **Nota**: Para rodar em segundo plano, você pode usar `nohup` ou `screen`:
    ```bash
    nohup flask run --host=0.0.0.0 --port=5000 > flask_output.log 2>&1 &
    ```

## 5. Endpoints da API (Resumo)

Aqui está um resumo dos principais endpoints da API. Para detalhes completos, consulte os arquivos em `src/routes/`.

### Autenticação (`/api/auth`)

*   `POST /register`: Registra um novo usuário.
*   `POST /login`: Autentica um usuário e retorna um token JWT.

### Usuários (`/api/users`)

*   `GET /profile`: Retorna o perfil do usuário autenticado.

### KYC (`/api/kyc`)

*   `POST /verify`: Inicia o processo de verificação KYC para o usuário autenticado.

### Score de Crédito (`/api/credit-score`)

*   `GET /`: Retorna o score de crédito do usuário autenticado.
*   `POST /calculate`: Calcula e atualiza o score de crédito do usuário.

### Empréstimos (`/api/loans`)

*   `POST /request`: Cria uma solicitação de empréstimo.
*   `POST /offer`: Cria uma oferta de empréstimo.
*   `GET /matches`: Lista os matches de empréstimo para o usuário.
*   `POST /match/<loan_match_id>/accept`: Aceita um match de empréstimo, criando um empréstimo ativo.
*   `GET /requests`: Lista as solicitações de empréstimo do usuário.
*   `GET /offers`: Lista as ofertas de empréstimo do usuário.
*   `GET /active`: Lista os empréstimos ativos do usuário (como devedor ou credor).

### Pagamentos (`/api/payments`)

*   `POST /installments/<installment_id>/pay`: Processa o pagamento de uma parcela.
*   `GET /transactions`: Lista as transações do usuário.
*   `GET /loans/<loan_id>/installments`: Lista as parcelas de um empréstimo específico.

## 6. Banco de Dados

O banco de dados `app.db` (SQLite) é criado e gerenciado pelo SQLAlchemy. As chaves estrangeiras são habilitadas através da string de conexão `sqlite:///app.db?foreign_keys=on` em `config.py`.

## 7. Testes

Atualmente, os testes são realizados manualmente via cURL. Para um ambiente de produção, testes unitários e de integração seriam implementados. Exemplos de comandos cURL para testar as APIs podem ser encontrados nos logs de execução do agente ou criados com base nos endpoints listados acima.

---
