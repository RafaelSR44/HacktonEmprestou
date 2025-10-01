
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.account_service import AccountService
from src.models.account import Account

accounts_bp = Blueprint("accounts", __name__)

@accounts_bp.route("/balance", methods=["GET"])
@jwt_required()
def get_balance():
    current_user_id = get_jwt_identity()
    balance = AccountService.get_account_balance(current_user_id)
    if balance is not None:
        return jsonify({"balance": str(balance)}), 200
    return jsonify({"message": "Conta não encontrada"}), 404

@accounts_bp.route("/deposit", methods=["POST"])
@jwt_required()
def deposit():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    amount = data.get("amount")

    if not amount or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"message": "Valor de depósito inválido"}), 400

    account, message = AccountService.deposit(current_user_id, amount)
    if account:
        return jsonify({"message": message, "balance": str(account.balance)}), 200
    return jsonify({"message": message}), 400

@accounts_bp.route("/withdraw", methods=["POST"])
@jwt_required()
def withdraw():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    amount = data.get("amount")

    if not amount or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"message": "Valor de saque inválido"}), 400

    account, message = AccountService.withdraw(current_user_id, amount)
    if account:
        return jsonify({"message": message, "balance": str(account.balance)}), 200
    return jsonify({"message": message}), 400

