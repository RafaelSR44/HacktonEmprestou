
from flask import Blueprint, request, jsonify
from src.services.auth_service import AuthService
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from src import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    whatsapp_id = data.get("whatsapp_id")
    full_name = data.get("full_name")
    cpf = data.get("cpf")
    birth_date = data.get("birth_date")

    if not all([whatsapp_id, full_name, cpf, birth_date]):
        return jsonify({"message": "Dados incompletos"}), 400

    try:
        user, created = AuthService.register_user(whatsapp_id, full_name, cpf, birth_date)
        if not created:
            return jsonify({"message": "Usuário já existe"}), 409
        
        access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(hours=1))
        return jsonify({"message": "Usuário registrado com sucesso", "access_token": access_token, "user": user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao registrar usuário", "error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    whatsapp_id = data.get("whatsapp_id")

    if not whatsapp_id:
        return jsonify({"message": "WhatsApp ID é obrigatório"}), 400

    user = AuthService.authenticate_user(whatsapp_id)
    if user:
        access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(hours=1))
        return jsonify({"message": "Login bem-sucedido", "access_token": access_token, "user": user.to_dict()}), 200
    else:
        return jsonify({"message": "Usuário não encontrado ou credenciais inválidas"}), 401

@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200

