from src.models.user import User
from src.models.account import Account
from src.models.credit_score import CreditScore
from src import db
from datetime import datetime

class AuthService:
    @staticmethod
    def register_user(whatsapp_id, full_name, cpf, birth_date):
        user = User.query.filter_by(whatsapp_id=whatsapp_id).first()
        if user:
            return user, False # Usuário já existe

        new_user = User(
            whatsapp_id=whatsapp_id,
            full_name=full_name,
            cpf=cpf,
            birth_date=datetime.strptime(birth_date, '%Y-%m-%d').date(),
            user_type='both' # Por padrão, pode ser credor e devedor
        )
        db.session.add(new_user)
        db.session.commit()

        # Criar conta para o novo usuário
        new_account = Account(user_id=new_user.user_id, account_type='digital_wallet')
        db.session.add(new_account)
        db.session.commit()

        # Criar entrada de score de crédito inicial (pode ser atualizado depois)
        initial_credit_score = CreditScore(user_id=new_user.user_id, score_value=0, score_provider='Initial')
        db.session.add(initial_credit_score)
        db.session.commit()

        return new_user, True

    @staticmethod
    def authenticate_user(whatsapp_id):
        user = User.query.filter_by(whatsapp_id=whatsapp_id).first()
        if user:
            # Em um cenário real, haveria um processo de verificação mais robusto (ex: OTP via WhatsApp)
            return user
        return None
