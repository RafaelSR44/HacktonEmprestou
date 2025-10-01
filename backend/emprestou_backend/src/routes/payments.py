from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.payment_service import PaymentService

payments_bp = Blueprint("payments", __name__)
payment_service = PaymentService()

@payments_bp.route("/installments/<installment_id>/pay", methods=["POST"])
@jwt_required()
def pay_installment(installment_id):
    current_user_id = get_jwt_identity()
    installment, message = payment_service.process_installment_payment(installment_id, current_user_id)
    if installment:
        return jsonify({"message": message, "installment": installment.to_dict()}), 200
    return jsonify({"message": message}), 400

@payments_bp.route("/transactions", methods=["GET"])
@jwt_required()
def get_transactions():
    current_user_id = get_jwt_identity()
    transactions, message = payment_service.get_user_transactions(current_user_id)
    return jsonify(transactions), 200

@payments_bp.route("/loans/<loan_id>/installments", methods=["GET"])
@jwt_required()
def get_loan_installments(loan_id):
    current_user_id = get_jwt_identity()
    installments, message = payment_service.get_loan_installments(loan_id, current_user_id)
    if installments:
        return jsonify(installments), 200
    return jsonify({"message": message}), 404

