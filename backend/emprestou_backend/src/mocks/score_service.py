import random
import uuid

class MockScoreService:
    def calculate_score(self, user_id):
        """Simula cálculo de score com ML"""
        # Gerar score aleatório mas consistente por usuário
        # Usar um hash do user_id para consistência, mas adicionar um pouco de aleatoriedade
        base_score = (hash(str(user_id)) % 600) + 300
        
        # Adicionar um pouco de variação para simular mudanças ao longo do tempo
        variation = random.randint(-50, 50)
        final_score = max(300, min(900, base_score + variation))

        return {
            "score": final_score,
            "classification": self._classify_score(final_score),
            "components": {
                "income": round(0.25 * final_score, 2),
                "debt_ratio": round(0.20 * final_score, 2),
                "payment_history": round(0.30 * final_score, 2),
                "external_score": round(0.20 * final_score, 2),
                "behavior": round(0.05 * final_score, 2)
            },
            "suggested_rate": self._calculate_rate(final_score),
            "max_amount": self._calculate_limit(final_score)
        }

    def _classify_score(self, score):
        if score >= 750:
            return "Excelente"
        elif score >= 700:
            return "Muito Bom"
        elif score >= 650:
            return "Bom"
        elif score >= 600:
            return "Regular"
        else:
            return "Baixo"

    def _calculate_rate(self, score):
        if score >= 750:
            return 2.0
        elif score >= 700:
            return 2.5
        elif score >= 650:
            return 3.0
        elif score >= 600:
            return 4.0
        else:
            return 5.0

    def _calculate_limit(self, score):
        if score >= 750:
            return 50000.00
        elif score >= 700:
            return 30000.00
        elif score >= 650:
            return 20000.00
        elif score >= 600:
            return 10000.00
        else:
            return 5000.00

