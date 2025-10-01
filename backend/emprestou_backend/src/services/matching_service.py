from src import db
from src.models import LoanRequest, LoanOffer, LoanMatch, Loan, User, Account, Transaction, Installment
from datetime import datetime, timedelta
from sqlalchemy import or_

class MatchingService:
    @staticmethod
    def find_matches(loan_request_id=None, loan_offer_id=None):
        matches_found = []

        if loan_request_id:
            loan_request = LoanRequest.query.get(loan_request_id)
            if not loan_request or loan_request.status != 'pending':
                return []
            
            # Encontrar ofertas que correspondam à solicitação
            # Simplificado para corresponder exatamente para o MVP
            matching_offers = LoanOffer.query.filter(
                LoanOffer.amount == loan_request.amount,
                LoanOffer.interest_rate <= loan_request.interest_rate,
                LoanOffer.installments == loan_request.installments,
                LoanOffer.status == 'pending'
            ).all()

            for offer in matching_offers:
                match = LoanMatch(
                    loan_request_id=loan_request.loan_request_id,
                    loan_offer_id=offer.loan_offer_id,
                    status='pending'
                )
                db.session.add(match)
                loan_request.status = 'matched' # Atualiza o status da solicitação
                offer.status = 'matched' # Atualiza o status da oferta
                db.session.commit()
                matches_found.append(match)
            return matches_found

        elif loan_offer_id:
            loan_offer = LoanOffer.query.get(loan_offer_id)
            if not loan_offer or loan_offer.status != 'pending':
                return []
            
            # Encontrar solicitações que correspondam à oferta
            # Simplificado para corresponder exatamente para o MVP
            matching_requests = LoanRequest.query.filter(
                LoanRequest.amount == loan_offer.amount,
                LoanRequest.interest_rate >= loan_offer.interest_rate,
                LoanRequest.installments == loan_offer.installments,
                LoanRequest.status == 'pending'
            ).all()

            for request in matching_requests:
                match = LoanMatch(
                    loan_request_id=request.loan_request_id,
                    loan_offer_id=loan_offer.loan_offer_id,
                    status='pending'
                )
                db.session.add(match)
                request.status = 'matched' # Atualiza o status da solicitação
                loan_offer.status = 'matched' # Atualiza o status da oferta
                db.session.commit()
                matches_found.append(match)
            return matches_found
        return []

    @staticmethod
    def accept_match(loan_match_id):
        loan_match = LoanMatch.query.get(loan_match_id)
        if not loan_match or loan_match.status != 'pending':
            return None, "Match não encontrado ou já processado."

        loan_request = LoanRequest.query.get(loan_match.loan_request_id)
        loan_offer = LoanOffer.query.get(loan_match.loan_offer_id)

        if not loan_request or not loan_offer:
            return None, "Solicitação ou oferta de empréstimo não encontrada."

        # Criar o empréstimo efetivo
        new_loan = Loan(
            loan_match_id=loan_match.loan_match_id,
            debtor_id=loan_request.user_id,
            creditor_id=loan_offer.user_id,
            principal_amount=loan_request.amount,
            interest_rate=loan_offer.interest_rate,
            installments=loan_request.installments,
            total_amount=loan_request.amount * (1 + (loan_offer.interest_rate / 100)), # Exemplo simples
            first_due_date=datetime.utcnow() + timedelta(days=30), # Primeira parcela em 30 dias
            status='active'
        )
        db.session.add(new_loan)
        db.session.flush() # Garante que o loan_id seja gerado e esteja disponível

        # Atualizar status
        loan_match.status = 'accepted'
        loan_request.status = 'approved'
        loan_offer.status = 'accepted'

        # Gerar parcelas
        MatchingService._generate_installments(new_loan)

        # Processar transações (desembolso para o devedor, crédito para o credor)
        MatchingService._process_loan_transactions(new_loan)

        db.session.commit()
        return new_loan, "Empréstimo aceito e criado com sucesso."

    @staticmethod
    def _generate_installments(loan):
        # Lógica para gerar parcelas (simplificada)
        # Em um cenário real, calcular juros compostos, etc.
        installment_amount = loan.total_amount / loan.installments
        for i in range(loan.installments):
            due_date = loan.first_due_date + timedelta(days=i * 30) # Exemplo: mensal
            installment = Installment(
                loan_id=loan.loan_id,
                installment_number=i + 1,
                due_date=due_date,
                amount_due=installment_amount,
                status='pending'
            )
            db.session.add(installment)

    @staticmethod
    def _process_loan_transactions(loan):
        # Desembolso para o devedor
        debtor_account = Account.query.filter_by(user_id=loan.debtor_id).first()
        if debtor_account:
            debtor_account.balance += loan.principal_amount
            transaction_debtor = Transaction(
                account_id=debtor_account.account_id,
                user_id=loan.debtor_id,
                transaction_type='loan_disbursement',
                amount=loan.principal_amount,
                description=f'Desembolso do empréstimo {loan.loan_id}',
                transaction_metadata={'loan_id': loan.loan_id}
            )
            db.session.add(transaction_debtor)

        # Crédito para o credor (o valor total do empréstimo é transferido para a conta do credor)
        creditor_account = Account.query.filter_by(user_id=loan.creditor_id).first()
        if creditor_account:
            # O credor não recebe o valor total do empréstimo imediatamente, mas sim as parcelas ao longo do tempo.
            # A transação inicial para o credor é mais um registro do empréstimo concedido.
            transaction_creditor = Transaction(
                account_id=creditor_account.account_id,
                user_id=loan.creditor_id,
                transaction_type='loan_granted',
                amount=-loan.principal_amount, # Negativo para indicar que o valor saiu da conta do credor
                description=f'Empréstimo concedido {loan.loan_id}, para {loan.debtor_id}, valor {loan.principal_amount}, taxa {loan.interest_rate}, parcelas {loan.installments}',
                transaction_metadata={'loan_id': loan.loan_id, 'debtor_id': loan.debtor_id}
            )
            db.session.add(transaction_creditor)

