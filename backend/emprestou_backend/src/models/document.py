
from src import db
from datetime import datetime
import uuid

class Document(db.Model):
    __tablename__ = 'documents'

    document_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False) # e.g., 'RG', 'CPF', 'Comprovante de Residencia'
    document_url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending') # 'pending', 'approved', 'rejected'
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    verification_data = db.Column(db.JSON) # Campo para armazenar dados de verificação do KYC

    def to_dict(self):
        return {
            'document_id': self.document_id,
            'user_id': self.user_id,
            'document_type': self.document_type,
            'document_url': self.document_url,
            'status': self.status,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'verified_at': self.verified_at.isoformat() if self.verified_at else None
        }

