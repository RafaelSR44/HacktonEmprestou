from src import db
from datetime import datetime
import uuid

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    transaction_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = db.Column(db.String(36), db.ForeignKey('accounts.account_id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    transaction_type = db.Column(db.String(50)) # 'deposit', 'withdrawal', 'loan_disbursement', etc
    amount = db.Column(db.Numeric(12,2))
    description = db.Column(db.Text)
    transaction_metadata = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'account_id': self.account_id,
            'user_id': self.user_id,
            'transaction_type': self.transaction_type,
            'amount': str(self.amount),
            'description': self.description,
            'metadata': self.transaction_metadata,
            'created_at': self.created_at.isoformat()
        }

