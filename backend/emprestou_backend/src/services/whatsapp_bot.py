
from src.mocks import MockWhatsAppAPI
from src.models import User, Account, LoanRequest, LoanOffer, CreditScore, Document
from src import db
from datetime import datetime
import re

class WhatsAppBot:
    def __init__(self, app=None):
        self.whatsapp_api = MockWhatsAppAPI(
            api_url=app.config["WHATSAPP_API_URL"],
            api_token=app.config["WHATSAPP_API_TOKEN"]
        ) if app else None
        self.app = app

    def init_app(self, app):
        self.whatsapp_api = MockWhatsAppAPI(
            api_url=app.config["WHATSAPP_API_URL"],
            api_token=app.config["WHATSAPP_API_TOKEN"]
        )
        self.app = app

    def process_message(self, from_number, message_body):
        with self.app.app_context():
            user = User.query.filter_by(whatsapp_id=from_number).first()

            if not user:
                return self._handle_registration(from_number, message_body)
            else:
                # Lógica para usuários existentes
                return self._handle_existing_user_message(user, message_body)

    def _handle_registration(self, from_number, message_body):
        # Simplesmente solicita o nome completo para registro inicial
        # Em um cenário real, haveria um fluxo de conversação mais complexo
        if "nome completo" in message_body.lower():
            full_name = message_body.strip()
            new_user = User(whatsapp_id=from_number, full_name=full_name)
            db.session.add(new_user)
            db.session.commit()
            self.whatsapp_api.send_message(from_number, f"Olá {full_name}! Bem-vindo(a) ao Emprestou. Para continuar, precisamos do seu CPF. Por favor, envie no formato XXX.XXX.XXX-XX.")
            return f"Usuário {full_name} registrado. Solicitando CPF."
        else:
            self.whatsapp_api.send_message(from_number, "Olá! Bem-vindo(a) ao Emprestou. Para começar, por favor, me diga seu nome completo.")
            return "Solicitando nome completo para registro."

    def _handle_existing_user_message(self, user, message_body):
        # Lógica para usuários existentes
        message_body_lower = message_body.lower()

        if not user.cpf:
            return self._handle_cpf_input(user, message_body)
        elif not user.birth_date:
            return self._handle_birth_date_input(user, message_body)
        elif not user.kyc_verified:
            return self._handle_kyc_flow(user, message_body)
        
        # Comandos principais
        if "solicitar empréstimo" in message_body_lower:
            self.whatsapp_api.send_message(user.whatsapp_id, "Qual valor você gostaria de solicitar?")
            # Implementar estado para aguardar o valor
            return "Aguardando valor do empréstimo."
        elif "oferecer empréstimo" in message_body_lower:
            self.whatsapp_api.send_message(user.whatsapp_id, "Qual valor você gostaria de oferecer?")
            # Implementar estado para aguardar o valor
            return "Aguardando valor da oferta."
        elif "meu saldo" in message_body_lower:
            account = Account.query.filter_by(user_id=user.user_id).first()
            if account:
                self.whatsapp_api.send_message(user.whatsapp_id, f"Seu saldo atual é de R$ {account.balance:.2f}.")
            else:
                self.whatsapp_api.send_message(user.whatsapp_id, "Não foi possível encontrar sua conta. Por favor, entre em contato com o suporte.")
            return "Informando saldo."
        elif "minhas solicitações" in message_body_lower:
            requests = LoanRequest.query.filter_by(user_id=user.user_id).all()
            if requests:
                response_msg = "Suas solicitações de empréstimo:\n"
                for req in requests:
                    response_msg += f"- ID: {req.loan_request_id}, Valor: R$ {req.amount:.2f}, Status: {req.status}\n"
                self.whatsapp_api.send_message(user.whatsapp_id, response_msg)
            else:
                self.whatsapp_api.send_message(user.whatsapp_id, "Você não possui solicitações de empréstimo ativas.")
            return "Informando solicitações de empréstimo."
        elif "minhas ofertas" in message_body_lower:
            offers = LoanOffer.query.filter_by(user_id=user.user_id).all()
            if offers:
                response_msg = "Suas ofertas de empréstimo:\n"
                for offer in offers:
                    response_msg += f"- ID: {offer.loan_offer_id}, Valor: R$ {offer.amount:.2f}, Taxa: {offer.interest_rate}%, Status: {offer.status}\n"
                self.whatsapp_api.send_message(user.whatsapp_id, response_msg)
            else:
                self.whatsapp_api.send_message(user.whatsapp_id, "Você não possui ofertas de empréstimo ativas.")
            return "Informando ofertas de empréstimo."
        else:
            self.whatsapp_api.send_message(user.whatsapp_id, "Desculpe, não entendi. Você pode tentar: 'Solicitar empréstimo', 'Oferecer empréstimo', 'Meu saldo', 'Minhas solicitações', 'Minhas ofertas'.")
            return "Mensagem não reconhecida."

    def _handle_cpf_input(self, user, message_body):
        cpf_pattern = re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
        if cpf_pattern.match(message_body):
            user.cpf = message_body
            db.session.commit()
            self.whatsapp_api.send_message(user.whatsapp_id, "Obrigado! Agora, por favor, informe sua data de nascimento no formato DD/MM/AAAA.")
            return "CPF recebido. Solicitando data de nascimento."
        else:
            self.whatsapp_api.send_message(user.whatsapp_id, "Formato de CPF inválido. Por favor, envie no formato XXX.XXX.XXX-XX.")
            return "CPF inválido."

    def _handle_birth_date_input(self, user, message_body):
        try:
            birth_date = datetime.strptime(message_body, "%d/%m/%Y").date()
            user.birth_date = birth_date
            db.session.commit()
            self.whatsapp_api.send_message(user.whatsapp_id, "Data de nascimento recebida. Para completar seu cadastro, precisamos verificar sua identidade (KYC). Por favor, envie uma foto do seu RG ou CNH.")
            return "Data de nascimento recebida. Iniciando fluxo KYC."
        except ValueError:
            self.whatsapp_api.send_message(user.whatsapp_id, "Formato de data de nascimento inválido. Por favor, envie no formato DD/MM/AAAA.")
            return "Data de nascimento inválida."

    def _handle_kyc_flow(self, user, message_body):
        # Simplificação: assume que qualquer mensagem com "foto" ou "documento" é uma tentativa de KYC
        # Em um cenário real, haveria upload de imagem e integração com o MockKYCService
        if "foto" in message_body.lower() or "documento" in message_body.lower():
            # Simula o envio de um documento para verificação
            # Aqui você integraria com o MockKYCService
            # Por enquanto, vamos aprovar automaticamente para fins de teste
            user.kyc_verified = True
            db.session.commit()
            self.whatsapp_api.send_message(user.whatsapp_id, "Documento recebido e verificado (simulado). Seu KYC foi aprovado! Agora você pode solicitar ou oferecer empréstimos.")
            return "KYC aprovado (simulado)."
        else:
            self.whatsapp_api.send_message(user.whatsapp_id, "Ainda precisamos verificar sua identidade. Por favor, envie uma foto do seu RG ou CNH para completar o KYC.")
            return "Aguardando documento para KYC."

