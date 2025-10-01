
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    return jsonify(user.to_dict()), 200

