from src import db
from datetime import datetime
import uuid

class LoanMatch(db.Model):
    __tablename__ = 'loan_matches'

    loan_match_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    loan_request_id = db.Column(db.String(36), db.ForeignKey('loan_requests.loan_request_id'), nullable=False)
    loan_offer_id = db.Column(db.String(36), db.ForeignKey('loan_offers.loan_offer_id'), nullable=False)
    matched_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending') # 'pending', 'accepted', 'rejected'

    # Relacionamento com Loan (o empréstimo efetivado)
    loan = db.relationship('Loan', backref='loan_match', uselist=False, lazy=True)

    def to_dict(self):
        return {
            'loan_match_id': self.loan_match_id,
            'loan_request_id': self.loan_request_id,
            'loan_offer_id': self.loan_offer_id,
            'matched_at': self.matched_at.isoformat(),
            'status': self.status
        }

