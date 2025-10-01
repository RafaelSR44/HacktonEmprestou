from src import db
from datetime import datetime
import uuid

class Loan(db.Model):
    __tablename__ = 'loans'

    loan_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    loan_match_id = db.Column(db.String(36), db.ForeignKey('loan_matches.loan_match_id'), unique=True, nullable=False)
    debtor_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    creditor_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    principal_amount = db.Column(db.Numeric(12, 2), nullable=False)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)

    interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    installments = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='active') # 'active', 'paid', 'defaulted'
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    first_due_date = db.Column(db.DateTime, nullable=False)

    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    installments_list = db.relationship('Installment', backref='loan', lazy=True)

    def to_dict(self):
        return {
            'loan_id': self.loan_id,
            'loan_match_id': self.loan_match_id,
            'debtor_id': self.debtor_id,
            'creditor_id': self.creditor_id,
            'principal_amount': str(self.principal_amount),
            'total_amount': str(self.total_amount),
            'interest_rate': str(self.interest_rate),
            'installments': self.installments,
            'status': self.status,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat()
        }

