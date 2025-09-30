# Prompt de Desenvolvimento - Projeto Emprestou (Hackathon QI 2024)

## Contexto do Projeto

Você deve desenvolver o **Emprestou**, uma plataforma P2P (peer-to-peer) de empréstimos via WhatsApp para o Hackathon QI 2024. Este é um MVP funcional focado em demonstrar o conceito e viabilidade técnica.

### Proposta de Valor
- Conectar credores e devedores diretamente via WhatsApp
- Taxas de juros negociáveis (2-6% a.m.) sem intermediários bancários
- Sistema de score de crédito com IA
- Matching inteligente entre ofertas e solicitações
- Anti-fraude com KYC completo
- Conta digital integrada

### Requisitos Obrigatórios do Hackathon
1. **Anti-fraude**: Validação de identidade (KYC) com documentos e biometria
2. **Score de Crédito**: Análise de risco e definição de taxas
3. **Funcionalidades P2P**: Marketplace de empréstimos com matching

---

## Stack Tecnológica

### Backend
- **Linguagem**: Python 3.11+
- **Framework**: Flask 3.0
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Database**: PostgreSQL 15
- **Cache**: Redis 7.0
- **Task Queue**: Celery + RabbitMQ (pode ser simplificado para apenas Redis no MVP)

### Frontend (Dashboard Administrativo)
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 3
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React

### Integrações (TODAS MOCKADAS)
- **WhatsApp**: Twilio API (mockar webhook e envio de mensagens)
- **Open Finance**: Pluggy/Belvo (mockar dados bancários)
- **PIX**: Stark Bank (mockar transações)
- **OCR/Biometria**: AWS Rekognition (mockar validação de documentos)
- **Score Externo**: Serasa/Boa Vista (mockar scores)

---

## Arquitetura Geral

```
emprestou/
├── backend/                 # API REST + Bot WhatsApp
│   ├── app/
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── services/        # Lógica de negócio
│   │   ├── api/             # Endpoints REST
│   │   ├── mocks/           # 🎭 APIs externas mockadas
│   │   └── utils/           # Utilitários
│   ├── migrations/          # Alembic migrations
│   ├── tests/               # Testes unitários
│   └── requirements.txt
│
├── frontend/                # Dashboard React
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── pages/           # Páginas
│   │   ├── services/        # API clients
│   │   └── store/           # Zustand stores
│   └── package.json
│
└── docker-compose.yml       # PostgreSQL + Redis local
```

---

## Funcionalidades Prioritárias (MVP)

### 🔴 ALTA PRIORIDADE (Obrigatório)

#### 1. Backend API Core

**1.1 Sistema de Autenticação e Usuários**
- Cadastro de usuários via WhatsApp (número como identificador único)
- Login com WhatsApp ID
- JWT tokens para autenticação
- Endpoints:
  - `POST /api/auth/register` - Cadastro inicial
  - `POST /api/auth/login` - Login
  - `GET /api/users/me` - Dados do usuário logado

**1.2 Sistema KYC (Know Your Customer)**
- Upload de documento (RG/CNH)
- Upload de selfie
- Validação mockada com score de confiança
- Endpoints:
  - `POST /api/kyc/upload-document` - Upload documento
  - `POST /api/kyc/upload-selfie` - Upload selfie
  - `GET /api/kyc/status` - Status da validação

**Mock necessário**:
```python
# app/mocks/kyc_service.py
class MockKYCService:
    def validate_document(self, image_data):
        """Simula OCR e validação de documento"""
        return {
            "valid": True,
            "confidence": 0.95,
            "extracted_data": {
                "name": "João Silva",
                "cpf": "123.456.789-00",
                "birth_date": "1990-01-01",
                "document_number": "12.345.678-9"
            }
        }
    
    def validate_face_match(self, doc_image, selfie_image):
        """Simula comparação facial"""
        return {
            "match": True,
            "confidence": 0.97,
            "liveness": True
        }
```

**1.3 Sistema de Score de Crédito**
- Cálculo de score baseado em dados mockados
- Score de 300-900
- Componentes: renda mockada, histórico, score externo mockado
- Endpoints:
  - `GET /api/credit-score` - Score do usuário
  - `POST /api/credit-score/calculate` - Recalcular score

**Mock necessário**:
```python
# app/mocks/score_service.py
class MockScoreService:
    def calculate_score(self, user_id):
        """Simula cálculo de score com ML"""
        # Gerar score aleatório mas consistente por usuário
        base_score = hash(str(user_id)) % 600 + 300
        return {
            "score": base_score,
            "classification": self._classify_score(base_score),
            "components": {
                "income": 0.25 * base_score,
                "debt_ratio": 0.20 * base_score,
                "payment_history": 0.30 * base_score,
                "external_score": 0.20 * base_score,
                "behavior": 0.05 * base_score
            },
            "suggested_rate": self._calculate_rate(base_score),
            "max_amount": self._calculate_limit(base_score)
        }
```

**1.4 Sistema de Empréstimos**
- CRUD de solicitações (requests)
- CRUD de ofertas (offers)
- Sistema de matching (algoritmo simples)
- Gestão de parcelas
- Endpoints:
  - `POST /api/loans/requests` - Criar solicitação
  - `GET /api/loans/requests` - Listar solicitações
  - `POST /api/loans/offers` - Criar oferta
  - `GET /api/loans/offers` - Listar ofertas
  - `POST /api/loans/match` - Criar match
  - `GET /api/loans/matches` - Listar matches
  - `POST /api/loans/{id}/approve` - Aprovar empréstimo
  - `GET /api/loans/{id}/installments` - Parcelas

**Mock de Matching**:
```python
# app/services/matching_service.py
class MatchingService:
    def find_matches(self, loan_request_id):
        """Algoritmo simples de matching"""
        request = LoanRequest.query.get(loan_request_id)
        
        # Buscar ofertas compatíveis
        compatible_offers = LoanOffer.query.filter(
            LoanOffer.amount >= request.amount,
            LoanOffer.interest_rate <= request.max_interest_rate,
            LoanOffer.max_installments >= request.installments,
            LoanOffer.min_score <= request.user.credit_score.score,
            LoanOffer.status == 'open'
        ).order_by(LoanOffer.interest_rate.asc()).limit(5).all()
        
        return compatible_offers
```

**1.5 Sistema de Contas e Transações**
- Conta digital para cada usuário
- Saldo disponível e bloqueado
- Transações (depósitos, saques, transferências)
- Endpoints:
  - `GET /api/accounts/balance` - Saldo da conta
  - `GET /api/accounts/transactions` - Histórico
  - `POST /api/accounts/deposit` - Depósito (mockado)
  - `POST /api/accounts/withdraw` - Saque (mockado)

**Mock necessário**:
```python
# app/mocks/payment_service.py
class MockPaymentService:
    def generate_pix_qrcode(self, amount):
        """Simula geração de QR Code PIX"""
        return {
            "qr_code": f"00020126580014br.gov.bcb.pix{uuid.uuid4()}",
            "qr_code_image": "data:image/png;base64,iVBORw0KGgoAAAANS...",
            "expires_at": datetime.now() + timedelta(minutes=15)
        }
    
    def process_pix_payment(self, qr_code, amount):
        """Simula processamento de pagamento PIX"""
        return {
            "status": "approved",
            "transaction_id": str(uuid.uuid4()),
            "paid_at": datetime.now().isoformat()
        }
```

#### 2. Bot WhatsApp Mockado

**2.1 Simulador de Conversas**
- Interface simples que simula chat do WhatsApp
- Processamento de comandos do usuário
- Respostas automáticas
- Estados da conversa (FSM - Finite State Machine)

**Implementação**:
```python
# app/services/whatsapp_bot.py
class WhatsAppBot:
    def __init__(self):
        self.states = {}  # {user_id: {"state": "...", "data": {...}}}
    
    def process_message(self, user_id, message):
        """Processa mensagem e retorna resposta"""
        state = self.states.get(user_id, {}).get("state", "idle")
        
        # FSM - Finite State Machine
        if state == "idle":
            return self._handle_idle(user_id, message)
        elif state == "requesting_loan":
            return self._handle_loan_request(user_id, message)
        elif state == "creating_offer":
            return self._handle_loan_offer(user_id, message)
        # ... outros estados
    
    def _handle_idle(self, user_id, message):
        """Detecta intenção e direciona fluxo"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["preciso", "empréstimo", "emprestar"]):
            self.states[user_id] = {"state": "requesting_loan", "data": {}}
            return "Quanto você precisa emprestar? Digite o valor."
        
        elif any(word in message_lower for word in ["investir", "emprestar dinheiro"]):
            self.states[user_id] = {"state": "creating_offer", "data": {}}
            return "Quanto você deseja disponibilizar para empréstimo?"
        
        # Menu padrão
        return self._get_menu()
```

**2.2 Endpoints do Bot**
- `POST /api/webhook/whatsapp` - Recebe mensagens (mock)
- `POST /api/bot/send` - Envia mensagem (mock, apenas loga)
- `GET /api/bot/conversations/{user_id}` - Histórico da conversa

**Mock necessário**:
```python
# app/mocks/whatsapp_api.py
class MockWhatsAppAPI:
    def __init__(self):
        self.message_log = []
    
    def send_message(self, to, message):
        """Simula envio de mensagem"""
        msg = {
            "to": to,
            "message": message,
            "sent_at": datetime.now().isoformat(),
            "status": "sent"
        }
        self.message_log.append(msg)
        return msg
    
    def get_conversation(self, user_id):
        """Retorna histórico"""
        return [msg for msg in self.message_log if msg["to"] == user_id]
```

#### 3. Database Schema

**Criar migrations Alembic para todas as tabelas:**

```sql
-- Tabelas principais (simplificadas para MVP)
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    whatsapp_id VARCHAR(20) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    full_name VARCHAR(200),
    email VARCHAR(200),
    birth_date DATE,
    user_type VARCHAR(20), -- 'creditor', 'debtor', 'both'
    kyc_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE accounts (
    account_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    balance DECIMAL(12,2) DEFAULT 0.00,
    blocked_balance DECIMAL(12,2) DEFAULT 0.00,
    currency VARCHAR(3) DEFAULT 'BRL',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE documents (
    document_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    document_type VARCHAR(20), -- 'rg', 'cnh', 'selfie'
    file_url TEXT,
    verified BOOLEAN DEFAULT FALSE,
    verification_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE credit_scores (
    score_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    score_value INTEGER CHECK (score_value BETWEEN 300 AND 900),
    score_details JSONB,
    calculated_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);

CREATE TABLE loan_requests (
    request_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    amount DECIMAL(12,2) NOT NULL,
    installments INTEGER NOT NULL,
    max_interest_rate DECIMAL(5,2),
    purpose TEXT,
    status VARCHAR(20) DEFAULT 'open', -- 'open', 'matched', 'cancelled'
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE loan_offers (
    offer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id),
    amount DECIMAL(12,2) NOT NULL,
    max_installments INTEGER,
    interest_rate DECIMAL(5,2) NOT NULL,
    min_score INTEGER,
    status VARCHAR(20) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE loan_matches (
    match_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    request_id UUID REFERENCES loan_requests(request_id),
    offer_id UUID REFERENCES loan_offers(offer_id),
    final_amount DECIMAL(12,2),
    final_installments INTEGER,
    final_interest_rate DECIMAL(5,2),
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'accepted', 'rejected'
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE loans (
    loan_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    match_id UUID REFERENCES loan_matches(match_id),
    debtor_id UUID REFERENCES users(user_id),
    creditor_id UUID REFERENCES users(user_id),
    principal_amount DECIMAL(12,2),
    interest_rate DECIMAL(5,2),
    installments INTEGER,
    total_amount DECIMAL(12,2),
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'completed', 'defaulted'
    first_due_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE installments (
    installment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    loan_id UUID REFERENCES loans(loan_id),
    installment_number INTEGER,
    amount DECIMAL(12,2),
    due_date DATE,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'paid', 'overdue'
    paid_at TIMESTAMP
);

CREATE TABLE transactions (
    transaction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    account_id UUID REFERENCES accounts(account_id),
    transaction_type VARCHAR(50), -- 'deposit', 'withdrawal', 'loan_disbursement', etc
    amount DECIMAL(12,2),
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_users_whatsapp ON users(whatsapp_id);
CREATE INDEX idx_users_cpf ON users(cpf);
CREATE INDEX idx_loan_requests_status ON loan_requests(status);
CREATE INDEX idx_loan_offers_status ON loan_offers(status);
CREATE INDEX idx_loans_status ON loans(status);
CREATE INDEX idx_installments_due ON installments(due_date, status);
```

#### 4. Dashboard Frontend Básico

**4.1 Páginas Principais**

1. **Login/Cadastro** (`/login`, `/register`)
   - Form simples com WhatsApp ID
   - Mock de autenticação

2. **Dashboard Home** (`/dashboard`)
   - Métricas gerais (cards com números)
   - Gráfico de transações (último 7 dias)
   - Lista de empréstimos ativos

3. **Empréstimos** (`/loans`)
   - Tabs: "Solicitações" | "Ofertas" | "Matches" | "Ativos"
   - Tabela com filtros básicos
   - Modal para criar nova solicitação/oferta

4. **Usuários** (`/users`)
   - Tabela de usuários
   - Status KYC
   - Score de crédito

5. **Minha Conta** (`/account`)
   - Saldo disponível
   - Extrato de transações
   - Botão de depósito (mock)

**4.2 Componentes Principais**

```typescript
// src/components/dashboard/StatsCard.tsx
interface StatsCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  change?: string;
}

export const StatsCard = ({ title, value, icon, change }: StatsCardProps) => (
  <div className="bg-white rounded-lg shadow p-6">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-gray-500 text-sm">{title}</p>
        <p className="text-2xl font-bold mt-2">{value}</p>
        {change && <p className="text-sm text-green-600 mt-1">{change}</p>}
      </div>
      <div className="text-blue-500">{icon}</div>
    </div>
  </div>
);

// src/components/loans/LoanRequestForm.tsx
export const LoanRequestForm = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    amount: '',
    installments: 12,
    maxInterestRate: 4.0,
    purpose: ''
  });

  // Form com validation e submit
};
```

**4.3 API Client**

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
});

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: (whatsappId: string) => api.post('/auth/login', { whatsapp_id: whatsappId }),
  register: (data: any) => api.post('/auth/register', data),
};

export const loanService = {
  createRequest: (data: any) => api.post('/loans/requests', data),
  getRequests: () => api.get('/loans/requests'),
  createOffer: (data: any) => api.post('/loans/offers', data),
  getOffers: () => api.get('/loans/offers'),
};
```

### 🟡 MÉDIA PRIORIDADE (Diferencial)

#### 5. IA de Negociação (Mockada)

**Funcionalidade**:
- Sugerir taxas de juros otimizadas
- Calcular probabilidade de aceitação de contra-proposta
- Recomendar ações

**Implementação**:
```python
# app/services/ai_negotiation.py
class AINotegotiationService:
    def analyze_counteroffer(self, match_id, proposed_rate):
        """Analisa contra-proposta e retorna recomendação"""
        match = LoanMatch.query.get(match_id)
        original_rate = match.offer.interest_rate
        
        # Lógica simplificada de IA (mock)
        rate_difference = ((original_rate - proposed_rate) / original_rate) * 100
        
        if rate_difference > 20:
            probability = 0.30
            recommendation = "reject"
        elif rate_difference > 10:
            probability = 0.60
            suggestion_rate = original_rate * 0.92
            recommendation = "counter"
        else:
            probability = 0.85
            recommendation = "accept"
        
        return {
            "probability_acceptance": probability,
            "recommendation": recommendation,
            "suggested_rate": suggestion_rate if recommendation == "counter" else None,
            "analysis": self._generate_analysis(match, rate_difference)
        }
```

#### 6. Simulador de WhatsApp UI

**Interface visual que simula WhatsApp**:
- Componente React que parece o WhatsApp
- Mostra conversas do bot
- Input para enviar mensagens
- Histórico de mensagens

```typescript
// src/components/whatsapp/ChatSimulator.tsx
export const ChatSimulator = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const userId = localStorage.getItem('user_id');

  const sendMessage = async () => {
    // Adiciona mensagem do usuário
    const userMsg = { from: 'user', text: input, timestamp: new Date() };
    setMessages([...messages, userMsg]);

    // Envia para bot e recebe resposta
    const response = await api.post('/bot/message', {
      user_id: userId,
      message: input
    });

    const botMsg = { from: 'bot', text: response.data.message, timestamp: new Date() };
    setMessages([...messages, userMsg, botMsg]);
    setInput('');
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header estilo WhatsApp */}
      <div className="bg-green-600 text-white p-4">
        <h2 className="text-lg font-semibold">Emprestou Bot</h2>
      </div>

      {/* Mensagens */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs px-4 py-2 rounded-lg ${
                msg.from === 'user'
                  ? 'bg-green-500 text-white'
                  : 'bg-white text-gray-800'
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="bg-white p-4 flex space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          className="flex-1 border rounded-full px-4 py-2"
          placeholder="Digite uma mensagem..."
        />
        <button
          onClick={sendMessage}
          className="bg-green-500 text-white rounded-full p-2"
        >
          Enviar
        </button>
      </div>
    </div>
  );
};
```

#### 7. Gestão de Parcelas e Pagamentos

- Visualização de parcelas a vencer
- Mock de pagamento de parcelas
- Atualização de status
- Cálculo de juros de mora

### 🟢 BAIXA PRIORIDADE (Se sobrar tempo)

#### 8. Features Extras
- Sistema de notificações (apenas visual, sem envio real)
- Filtros avançados nas tabelas
- Export de dados (CSV)
- Temas claro/escuro
- Gráficos mais elaborados

---

## Estrutura de Código Detalhada

### Backend

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    from app.api.routes import auth, users, loans, accounts, kyc, bot
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(loans.bp)
    app.register_blueprint(accounts.bp)
    app.register_blueprint(kyc.bp)
    app.register_blueprint(bot.bp)
    
    return app


# app/models/user.py
from app import db
from datetime import datetime
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    whatsapp_id = db.Column(db.String(20), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    full_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    user_type = db.Column(db.String(20))
    kyc_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    account = db.relationship('Account', backref='user', uselist=False)
    documents = db.relationship('Document', backref='user')
    credit_score = db.relationship('CreditScore', backref='user', uselist=False)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'whatsapp_id': self.whatsapp_id,
            'full_name': self.full_name,
            'user_type': self.user_type,
            'kyc_verified': self.kyc_verified,
            'created_at': self.created_at.isoformat()
        }


# app/api/routes/loans.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.matching_service import MatchingService
from app.models.loan import LoanRequest, LoanOffer
from app import db

bp = Blueprint('loans', __name__, url_prefix='/api/loans')

@bp.route('/requests', methods=['POST'])
@jwt_required()
def create_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    loan_request = LoanRequest(
        user_id=user_id,
        amount=data['amount'],
        installments=data['installments'],
        max_interest_rate=data['max_interest_rate'],
        purpose=data.get('purpose')
    )
    
    db.session.add(loan_request)
    db.session.commit()
    
    # Buscar matches
    matching_service = MatchingService()
    matches = matching_service.find_matches(loan_request.request_id)
    
    return jsonify({
        'request': loan_request.to_dict(),
        'matches': [m.to_dict() for m in matches]
    }), 201


# app/mocks/open_finance.py
class MockOpenFinanceService:
    def get_bank_accounts(self, user_id):
        """Simula dados de contas bancárias"""
        return {
            "accounts": [
                {
                    "bank": "Nubank",
                    "type": "checking",
                    "balance": 5420.50,
                    "currency": "BRL"
                }
            ]
        }
    
    def get_income_analysis(self, user_id):
        """Simula análise de renda"""
        return {
            "monthly_income": 4500.00,
            "income_stability": 0.85,
            "income_sources": ["salary"],
            "last_12_months_avg": 4350.00
        }
    
    def get_debt_analysis(self, user_id):
        """Simula análise de dívidas"""
        return {
            "total_debt": 1200.00,
            "debt_to_income_ratio": 0.27,
            "active_loans": 1,
            "credit_card_usage": 0.35
        }


# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/emprestou'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
```

### Frontend

```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Loans } from './pages/Loans';
import { Users } from './pages/Users';
import { Account } from './pages/Account';
import { ChatSimulator } from './pages/ChatSimulator';
import { PrivateRoute } from './components/PrivateRoute';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />
        <Route path="/loans" element={
          <PrivateRoute>
            <Loans />
          </PrivateRoute>
        } />
        <Route path="/chat" element={
          <PrivateRoute>
            <ChatSimulator />
          </PrivateRoute>
        } />
        <Route path="/" element={<Navigate to="/dashboard" />} />
      </Routes>
    </BrowserRouter>
  );
}


// src/store/authStore.ts
import create from 'zustand';

interface AuthState {
  token: string | null;
  user: any | null;
  login: (token: string, user: any) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  login: (token, user) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
    set({ token, user });
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({ token: null, user: null });
  },
}));
```

---

## Docker Compose para Desenvolvimento

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: emprestou
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## Comandos de Setup

### Backend
```bash
cd backend

# Criar virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install flask flask-sqlalchemy flask-migrate flask-jwt-extended flask-cors psycopg2-binary redis celery pillow

# Gerar requirements.txt
pip freeze > requirements.txt

# Criar banco de dados
docker-compose up -d postgres redis

# Rodar migrations
flask db init
flask db migrate -m "Initial schema"
flask db upgrade

# Rodar servidor
flask run
```

### Frontend
```bash
cd frontend

# Criar projeto Vite + React
npm create vite@latest . -- --template react-ts

# Instalar dependências
npm install react-router-dom axios zustand recharts lucide-react
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Rodar desenvolvimento
npm run dev
```

---

## Checklist de Desenvolvimento

- [ ] Setup inicial
  - [ ] Criar repositório
  - [ ] Setup Docker Compose
  - [ ] Setup backend Flask
  - [ ] Setup frontend React
  - [ ] Rodar migrations iniciais

- [ ] Backend Core
  - [ ] Modelos SQLAlchemy
  - [ ] Endpoints de autenticação
  - [ ] Endpoints de KYC (com mocks)
  - [ ] Sistema de score (mockado)
  - [ ] Endpoints de empréstimos
  - [ ] Matching básico

- [ ] Dashboard Básico
  - [ ] Tela de login
  - [ ] Dashboard home
  - [ ] Tela de empréstimos
  - [ ] Integração com API

- [ ] Bot WhatsApp
  - [ ] FSM básica
  - [ ] Endpoints do bot
  - [ ] Lógica de comandos

- [ ] Finalizações
  - [ ] Simulador WhatsApp UI
  - [ ] IA de negociação (mock)
  - [ ] Gestão de parcelas
  - [ ] Seeds de dados

- [ ] Testes e Ajustes
  - [ ] Testar fluxos completos
  - [ ] Corrigir bugs críticos
  - [ ] Melhorias de UX

- [ ] Apresentação
  - [ ] Preparar demo
  - [ ] Documentar features
  - [ ] Screenshots/vídeo

---

## Seeds de Dados para Demo

```python
# scripts/seed_data.py
from app import create_app, db
from app.models import User, Account, CreditScore, LoanRequest, LoanOffer
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    # Criar usuários de exemplo
    users_data = [
        {"whatsapp_id": "5511999999999", "full_name": "João Silva", "user_type": "both", "kyc_verified": True},
        {"whatsapp_id": "5511888888888", "full_name": "Maria Santos", "user_type": "creditor", "kyc_verified": True},
        {"whatsapp_id": "5511777777777", "full_name": "Pedro Costa", "user_type": "debtor", "kyc_verified": True},
    ]
    
    for user_data in users_data:
        user = User(**user_data)
        db.session.add(user)
        db.session.flush()
        
        # Criar conta
        account = Account(user_id=user.user_id, balance=random.uniform(1000, 50000))
        db.session.add(account)
        
        # Criar score
        score = CreditScore(
            user_id=user.user_id,
            score_value=random.randint(600, 850),
            calculated_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        db.session.add(score)
    
    db.session.commit()
    
    # Criar solicitações de empréstimo
    requests_data = [
        {"amount": 5000, "installments": 12, "max_interest_rate": 4.0, "purpose": "Reforma da casa"},
        {"amount": 3000, "installments": 6, "max_interest_rate": 3.5, "purpose": "Compra de moto"},
    ]
    
    for req in requests_data:
        loan_req = LoanRequest(user_id=User.query.filter_by(user_type="debtor").first().user_id, **req)
        db.session.add(loan_req)
    
    # Criar ofertas
    offers_data = [
        {"amount": 10000, "max_installments": 18, "interest_rate": 3.2, "min_score": 700},
        {"amount": 5000, "max_installments": 12, "interest_rate": 4.5, "min_score": 600},
    ]
    
    for offer in offers_data:
        loan_offer = LoanOffer(user_id=User.query.filter_by(user_type="creditor").first().user_id, **offer)
        db.session.add(loan_offer)
    
    db.session.commit()
    print("Seeds criados com sucesso!")
```

---

## Pontos de Atenção

### ✅ O QUE FAZER
1. **Focar no MVP**: Implementar apenas o essencial para a demo
2. **Mockar tudo externo**: APIs de terceiros devem ser mocks
3. **Usar dados realistas**: Seeds com dados que fazem sentido
4. **Testar fluxos completos**: Garantir que a demo funciona end-to-end
5. **Commits frequentes**: Fazer commits a cada feature completa
6. **README claro**: Instruções de setup e execução

### ❌ O QUE NÃO FAZER
1. Não integrar APIs reais (sem credenciais, sem custos)
2. Não fazer over-engineering (KISS - Keep It Simple, Stupid)
3. Não adicionar features fora do MVP
4. Não se preocupar com deploy em produção
5. Não fazer autenticação complexa (JWT simples basta)
6. Não otimizar prematuramente

---

## Critérios de Avaliação QI

Lembre-se dos critérios que a banca avaliará:

1. **Produto e Valor Entregue** (35%)
   - Funcionalidade completa do MVP
   - Qualidade da experiência do usuário
   - Inovação e diferenciação

2. **Justificativa das Escolhas Técnicas** (25%)
   - Por que Python/Flask/React?
   - Por que mockar ao invés de integrar?
   - Escalabilidade da solução

3. **Segurança Cibernética** (20%)
   - Criptografia de dados sensíveis
   - Validação de inputs
   - Autenticação JWT
   - Logs de auditoria

4. **Qualidade da Apresentação** (15%)
   - Clareza na explicação
   - Demo funcionando
   - Documentação

5. **Modelo de Negócio** (5%)
   - Como ganha dinheiro
   - Sustentabilidade

---

## Resultado Esperado

Ao final das 30 horas, você deve ter:

✅ Backend Flask funcional com todas as APIs principais
✅ Frontend React com dashboard administrativo
✅ Simulador de WhatsApp funcionando
✅ Fluxo completo: cadastro → KYC → score → solicitar/ofertar → match → empréstimo
✅ Dados seed para demonstração
✅ README com instruções de setup
✅ Apresentação preparada

**BOA SORTE NO HACKATHON! 🚀**