
from src import db
from datetime import datetime
import uuid

class LoanRequest(db.Model):
    __tablename__ = 'loan_requests'

    loan_request_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2))
    installments = db.Column(db.Integer)
    status = db.Column(db.String(50), default='pending') # 'pending', 'approved', 'rejected', 'matched'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    loan_offers = db.relationship('LoanOffer', backref='loan_request', lazy=True)
    loan_matches = db.relationship('LoanMatch', backref='loan_request', lazy=True)

    def to_dict(self):
        return {
            'loan_request_id': self.loan_request_id,
            'user_id': self.user_id,
            'amount': str(self.amount),
            'interest_rate': str(self.interest_rate) if self.interest_rate else None,
            'installments': self.installments,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

