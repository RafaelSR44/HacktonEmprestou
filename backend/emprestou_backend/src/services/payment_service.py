from src import db
from src.models import Installment, Account, Transaction, Loan
from src.mocks.payment_service import MockPaymentService
from datetime import datetime

class PaymentService:
    def __init__(self):
        self.mock_payment_service = MockPaymentService()

    def process_installment_payment(self, installment_id, user_id):
        installment = Installment.query.get(installment_id)
        if not installment:
            return None, "Parcela não encontrada."

        if installment.status == 'paid':
            return None, "Parcela já paga."

        loan = Loan.query.get(installment.loan_id)
        if not loan:
            return None, "Empréstimo associado à parcela não encontrado."

        # Verifica se o usuário que está pagando é o devedor do empréstimo
        if user_id != loan.debtor_id:
            return None, "Você não é o devedor deste empréstimo."

        debtor_account = Account.query.filter_by(user_id=loan.debtor_id).first()
        creditor_account = Account.query.filter_by(user_id=loan.creditor_id).first()

        if not debtor_account or not creditor_account:
            return None, "Contas de devedor ou credor não encontradas."

        if debtor_account.balance < installment.amount_due:
            return None, "Saldo insuficiente para pagar a parcela."

        # Simula o processamento do pagamento
        payment_result = self.mock_payment_service.process_payment(
            account_id=debtor_account.account_id,
            amount=installment.amount_due,
            description=f"Pagamento da parcela {installment.installment_number} do empréstimo {loan.loan_id}"
        )

        if payment_result["status"] == "completed":
            # Atualiza o saldo do devedor
            debtor_account.balance -= installment.amount_due
            # Atualiza o saldo do credor
            creditor_account.balance += installment.amount_due

            # Cria transação para o devedor
            transaction_debtor = Transaction(
                account_id=debtor_account.account_id,
                user_id=loan.debtor_id,
                transaction_type='installment_payment',
                amount=-installment.amount_due,
                description=f'Pagamento da parcela {installment.installment_number} do empréstimo {loan.loan_id}',
                transaction_metadata={'loan_id': loan.loan_id, 'installment_id': installment.installment_id}
            )
            db.session.add(transaction_debtor)

            # Cria transação para o credor
            transaction_creditor = Transaction(
                account_id=creditor_account.account_id,
                user_id=loan.creditor_id,
                transaction_type='installment_receipt',
                amount=installment.amount_due,
                description=f'Recebimento da parcela {installment.installment_number} do empréstimo {loan.loan_id}',
                transaction_metadata={'loan_id': loan.loan_id, 'installment_id': installment.installment_id}
            )
            db.session.add(transaction_creditor)

            # Atualiza o status da parcela
            installment.status = 'paid'
            installment.amount_paid = installment.amount_due
            installment.paid_at = datetime.utcnow()

            db.session.commit()
            return installment, "Pagamento da parcela processado com sucesso."
        else:
            return None, "Falha ao processar o pagamento da parcela."

    def get_user_transactions(self, user_id):
        transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
        return [t.to_dict() for t in transactions], "Transações recuperadas com sucesso."

    def get_loan_installments(self, loan_id, user_id):
        loan = Loan.query.get(loan_id)
        if not loan:
            return None, "Empréstimo não encontrado."
        
        # Verifica se o usuário tem permissão para ver as parcelas (devedor ou credor)
        if user_id not in [loan.debtor_id, loan.creditor_id]:
            return None, "Você não tem permissão para visualizar as parcelas deste empréstimo."

        installments = Installment.query.filter_by(loan_id=loan_id).order_by(Installment.installment_number).all()
        return [i.to_dict() for i in installments], "Parcelas recuperadas com sucesso."

