from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.credit_score_service import CreditScoreService

credit_score_bp = Blueprint("credit_score", __name__)
credit_score_service = CreditScoreService()

@credit_score_bp.route("/", methods=["GET"])
@jwt_required()
def get_credit_score():
    current_user_id = get_jwt_identity()
    credit_score, message = credit_score_service.get_user_credit_score(current_user_id)
    if credit_score:
        return jsonify(credit_score.to_dict()), 200
    return jsonify({"message": message}), 404

@credit_score_bp.route("/calculate", methods=["POST"])
@jwt_required()
def calculate_credit_score():
    current_user_id = get_jwt_identity()
    credit_score, message = credit_score_service.calculate_and_update_score(current_user_id)
    if credit_score:
        return jsonify(credit_score.to_dict()), 200
    return jsonify({"message": message}), 400

