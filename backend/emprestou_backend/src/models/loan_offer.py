from src import db
from datetime import datetime
import uuid

class LoanOffer(db.Model):
    __tablename__ = 'loan_offers'

    loan_offer_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    loan_request_id = db.Column(db.String(36), db.ForeignKey('loan_requests.loan_request_id'), nullable=True) # Pode ser uma oferta proativa
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    installments = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='pending') # 'pending', 'accepted', 'rejected', 'matched'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    loan_matches = db.relationship('LoanMatch', backref='loan_offer', lazy=True)

    def to_dict(self):
        return {
            'loan_offer_id': self.loan_offer_id,
            'user_id': self.user_id,
            'loan_request_id': self.loan_request_id,
            'amount': str(self.amount),
            'interest_rate': str(self.interest_rate),
            'installments': self.installments,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

