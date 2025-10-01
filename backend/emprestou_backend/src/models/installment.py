from src import db
from datetime import datetime
import uuid

class Installment(db.Model):
    __tablename__ = 'installments'

    installment_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    loan_id = db.Column(db.String(36), db.ForeignKey('loans.loan_id'), nullable=False)
    installment_number = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    amount_due = db.Column(db.Numeric(12, 2), nullable=False)
    amount_paid = db.Column(db.Numeric(12, 2), default=0.00)
    status = db.Column(db.String(50), default='pending') # 'pending', 'paid', 'overdue'
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'installment_id': self.installment_id,
            'loan_id': self.loan_id,
            'installment_number': self.installment_number,
            'due_date': self.due_date.isoformat(),
            'amount_due': str(self.amount_due),
            'amount_paid': str(self.amount_paid),
            'status': self.status,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'created_at': self.created_at.isoformat()
        }

