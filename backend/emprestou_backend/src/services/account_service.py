from src.models.account import Account
from src.models.transaction import Transaction
from src import db
from datetime import datetime

class AccountService:
    @staticmethod
    def get_account_balance(user_id):
        account = Account.query.filter_by(user_id=user_id).first()
        if account:
            return account.balance
        return None

    @staticmethod
    def deposit(user_id, amount, description="Depósito via plataforma"):
        account = Account.query.filter_by(user_id=user_id).first()
        if not account:
            return None, "Conta não encontrada."
        
        account.balance += amount
        transaction = Transaction(
            account_id=account.account_id,
            user_id=user_id,
            transaction_type='deposit',
            amount=amount,
            description=description
        )
        db.session.add(transaction)
        db.session.commit()
        return account, "Depósito realizado com sucesso."

    @staticmethod
    def withdraw(user_id, amount, description="Saque via plataforma"):
        account = Account.query.filter_by(user_id=user_id).first()
        if not account:
            return None, "Conta não encontrada."
        
        if account.balance < amount:
            return None, "Saldo insuficiente."

        account.balance -= amount
        transaction = Transaction(
            account_id=account.account_id,
            user_id=user_id,
            transaction_type='withdrawal',
            amount=-amount, # Valor negativo para saque
            description=description
        )
        db.session.add(transaction)
        db.session.commit()
        return account, "Saque realizado com sucesso."

