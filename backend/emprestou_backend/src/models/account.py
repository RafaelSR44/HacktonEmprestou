
from src import db
from datetime import datetime
import uuid

class Account(db.Model):
    __tablename__ = 'accounts'
    
    account_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    balance = db.Column(db.Numeric(12, 2), default=0.00)
    account_type = db.Column(db.String(50)) # 'digital_wallet'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'balance': str(self.balance),
            'account_type': self.account_type,
            'created_at': self.created_at.isoformat()
        }

