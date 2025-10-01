
from src import db
from datetime import datetime
import uuid

class CreditScore(db.Model):
    __tablename__ = 'credit_scores'

    score_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), unique=True, nullable=False)
    score_value = db.Column(db.Integer, nullable=False)
    score_provider = db.Column(db.String(100))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'score_id': self.score_id,
            'user_id': self.user_id,
            'score_value': self.score_value,
            'score_provider': self.score_provider,
            'last_updated': self.last_updated.isoformat()
        }

