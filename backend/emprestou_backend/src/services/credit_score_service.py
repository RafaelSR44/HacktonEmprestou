from src.models.user import User
from src.models.credit_score import CreditScore
from src.mocks.score_service import MockScoreService
from src import db
from datetime import datetime

class CreditScoreService:
    def __init__(self):
        self.mock_score_service = MockScoreService()

    def calculate_and_update_score(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuário não encontrado."

        score_data = self.mock_score_service.calculate_score(user_id)

        credit_score_entry = CreditScore.query.filter_by(user_id=user_id).first()
        if credit_score_entry:
            credit_score_entry.score_value = score_data["score"]
            credit_score_entry.score_provider = "MockScoreService"
            credit_score_entry.last_updated = datetime.utcnow()
            # Adicionar mais campos se o modelo CreditScore for expandido para JSONB
        else:
            credit_score_entry = CreditScore(
                user_id=user_id,
                score_value=score_data["score"],
                score_provider="MockScoreService"
            )
            db.session.add(credit_score_entry)
        
        db.session.commit()
        return credit_score_entry, "Score de crédito atualizado com sucesso."

    def get_user_credit_score(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuário não encontrado."
        
        credit_score_entry = CreditScore.query.filter_by(user_id=user_id).first()
        if credit_score_entry:
            return credit_score_entry, "Score de crédito recuperado com sucesso."
        return None, "Score de crédito não encontrado para este usuário."

