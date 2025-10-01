from datetime import datetime
import uuid

class MockPaymentService:
    def process_payment(self, account_id, amount, description):
        print(f"MockPaymentService: Processando pagamento de {amount} para a conta {account_id} - {description}")
        payment_id = str(uuid.uuid4())
        # Simula um processamento de pagamento bem-sucedido
        return {
            "status": "completed",
            "payment_id": payment_id,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat(),
            "description": description
        }

    def process_receipt(self, account_id, amount, description):
        print(f"MockPaymentService: Processando recebimento de {amount} para a conta {account_id} - {description}")
        receipt_id = str(uuid.uuid4())
        # Simula um processamento de recebimento bem-sucedido
        return {
            "status": "completed",
            "receipt_id": receipt_id,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat(),
            "description": description
        }

