from src.models.user import User
from src.models.document import Document
from src.mocks.kyc_service import MockKYCService # Importa diretamente o mock
from src import db
from datetime import datetime

class KYCService:
    def __init__(self, app=None):
        self.mock_kyc_service = MockKYCService() # Instancia o mock
        self.app = app

    def init_app(self, app):
        self.app = app

    def upload_document(self, user_id, document_type, document_url):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuário não encontrado."

        # Simula a validação do documento usando o mock
        # Para simplificar, image_data será o document_url por enquanto
        validation_result = self.mock_kyc_service.validate_document(document_url)
        
        if validation_result["valid"]:
            new_document = Document(
                user_id=user_id,
                document_type=document_type,
                document_url=document_url,
                status='approved',
                verification_data=validation_result["extracted_data"]
            )
            db.session.add(new_document)
            user.kyc_verified = True # Atualiza o status KYC do usuário
            db.session.commit()
            return new_document, "Documento aprovado e KYC verificado."
        else:
            new_document = Document(
                user_id=user_id,
                document_type=document_type,
                document_url=document_url,
                status='rejected',
                verification_data=validation_result # Armazena o resultado completo da validação
            )
            db.session.add(new_document)
            db.session.commit()
            return new_document, f"Documento rejeitado: {validation_result.get('message', 'Motivo desconhecido')}"

    def get_user_kyc_status(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuário não encontrado."
        
        documents = Document.query.filter_by(user_id=user_id).all()
        kyc_status = {
            "user_id": user.user_id,
            "kyc_verified": user.kyc_verified,
            "documents": [doc.to_dict() for doc in documents]
        }
        return kyc_status, "Status KYC recuperado com sucesso."

