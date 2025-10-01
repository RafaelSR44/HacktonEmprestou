from src import db
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
    user_type = db.Column(db.String(20)) # 'creditor', 'debtor', 'both'
    kyc_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    account = db.relationship('Account', backref='user', uselist=False, lazy=True)
    documents = db.relationship('Document', backref='user', lazy=True)
    credit_score = db.relationship('CreditScore', backref='user', uselist=False, lazy=True)
    loan_requests = db.relationship('LoanRequest', backref='user', lazy=True)
    loan_offers = db.relationship('LoanOffer', backref='user', lazy=True)
    loans_as_debtor = db.relationship('Loan', foreign_keys='Loan.debtor_id', backref='debtor_user', lazy=True)
    loans_as_creditor = db.relationship('Loan', foreign_keys='Loan.creditor_id', backref='creditor_user', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'whatsapp_id': self.whatsapp_id,
            'full_name': self.full_name,
            'user_type': self.user_type,
            'kyc_verified': self.kyc_verified,
            'created_at': self.created_at.isoformat()
        }
