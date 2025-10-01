import uuid
from datetime import datetime, timedelta

class MockKYCService:
    def validate_document(self, image_data):
        """Simula OCR e validação de documento"""
        # Para simulação, sempre retorna válido por enquanto
        return {
            "valid": True,
            "confidence": 0.95,
            "extracted_data": {
                "name": "João Silva",
                "cpf": "123.456.789-00",
                "birth_date": "1990-01-01",
                "document_number": "12.345.678-9"
            },
            "message": "Documento validado com sucesso."
        }
    
    def validate_face_match(self, doc_image, selfie_image):
        """Simula comparação facial"""
        return {
            "match": True,
            "confidence": 0.97,
            "liveness": True,
            "message": "Correspondência facial verificada com sucesso."
        }

