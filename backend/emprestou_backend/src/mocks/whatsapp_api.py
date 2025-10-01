import requests

class MockWhatsAppAPI:
    def __init__(self, api_url, api_token):
        self.api_url = api_url
        self.api_token = api_token

    def send_message(self, to, message):
        print(f"MockWhatsAppAPI: Enviando mensagem para {to}: {message}")
        # Simula o envio de uma mensagem via WhatsApp
        # Em um cenário real, faria uma requisição HTTP para a API do WhatsApp
        try:
            # response = requests.post(f"{self.api_url}/send", json={
            #     "to": to,
            #     "message": message,
            #     "token": self.api_token
            # })
            # response.raise_for_status()
            # return response.json()
            return {"status": "success", "message_id": "mock_whatsapp_msg_123"}
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar mensagem mock do WhatsApp: {e}")
            return {"status": "error", "message": str(e)}

