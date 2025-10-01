
from flask import Blueprint, request, jsonify, current_app
from src.services.whatsapp_bot import WhatsAppBot

bot_bp = Blueprint("bot", __name__)

# Instancia o bot fora da rota para que ele possa ser inicializado com o app
whatsapp_bot = WhatsAppBot()

@bot_bp.before_app_request
def init_bot():
    whatsapp_bot.init_app(current_app)

@bot_bp.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.get_json()
    from_number = data.get("from")
    message_body = data.get("body")

    if not all([from_number, message_body]):
        return jsonify({"message": "Dados incompletos"}), 400

    response_message = whatsapp_bot.process_message(from_number, message_body)
    return jsonify({"message": "Mensagem processada", "bot_response": response_message}), 200

