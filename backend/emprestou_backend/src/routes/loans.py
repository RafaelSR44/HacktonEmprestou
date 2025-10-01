
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src import db
from src.models.loan_request import LoanRequest
from src.models.loan_offer import LoanOffer
from src.models.loan_match import LoanMatch
from src.models.loan import Loan
from src.services.matching_service import MatchingService

loans_bp = Blueprint("loans", __name__)

@loans_bp.route("/request", methods=["POST"])
@jwt_required()
def create_loan_request():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    amount = data.get("amount")
    interest_rate = data.get("interest_rate")
    installments = data.get("installments")

    if not all([amount, installments]):
        return jsonify({"message": "Valor e número de parcelas são obrigatórios"}), 400

    try:
        new_request = LoanRequest(
            user_id=current_user_id,
            amount=amount,
            interest_rate=interest_rate,
            installments=installments
        )
        db.session.add(new_request)
        db.session.commit()

        # Tentar encontrar matches imediatamente
        MatchingService.find_matches(loan_request_id=new_request.loan_request_id)

        return jsonify({"message": "Solicitação de empréstimo criada com sucesso", "loan_request": new_request.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao criar solicitação de empréstimo", "error": str(e)}), 500

@loans_bp.route("/offer", methods=["POST"])
@jwt_required()
def create_loan_offer():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    amount = data.get("amount")
    interest_rate = data.get("interest_rate")
    installments = data.get("installments")
    loan_request_id = data.get("loan_request_id") # Opcional, se for uma oferta para uma solicitação específica

    if not all([amount, interest_rate, installments]):
        return jsonify({"message": "Valor, taxa de juros e número de parcelas são obrigatórios"}), 400

    try:
        new_offer = LoanOffer(
            user_id=current_user_id,
            loan_request_id=loan_request_id,
            amount=amount,
            interest_rate=interest_rate,
            installments=installments
        )
        db.session.add(new_offer)
        db.session.commit()

        # Tentar encontrar matches imediatamente
        MatchingService.find_matches(loan_offer_id=new_offer.loan_offer_id)

        return jsonify({"message": "Oferta de empréstimo criada com sucesso", "loan_offer": new_offer.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao criar oferta de empréstimo", "error": str(e)}), 500

@loans_bp.route("/match/<loan_match_id>/accept", methods=["POST"])
@jwt_required()
def accept_loan_match(loan_match_id):
    current_user_id = get_jwt_identity()
    loan_match = LoanMatch.query.get(loan_match_id)

    if not loan_match:
        return jsonify({"message": "Match de empréstimo não encontrado"}), 404

    loan_request = LoanRequest.query.get(loan_match.loan_request_id)
    loan_offer = LoanOffer.query.get(loan_match.loan_offer_id)

    # Verifica se o usuário atual é o devedor ou o credor do match
    if not (current_user_id == loan_request.user_id or current_user_id == loan_offer.user_id):
        return jsonify({"message": "Você não tem permissão para aceitar este match"}), 403

    try:
        loan, message = MatchingService.accept_match(loan_match_id)
        if loan:
            return jsonify({"message": message, "loan": loan.to_dict()}), 200
        else:
            return jsonify({"message": message}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao aceitar match de empréstimo", "error": str(e)}), 500

@loans_bp.route("/requests", methods=["GET"])
@jwt_required()
def get_loan_requests():
    current_user_id = get_jwt_identity()
    requests = LoanRequest.query.filter_by(user_id=current_user_id).all()
    return jsonify([req.to_dict() for req in requests]), 200

@loans_bp.route("/offers", methods=["GET"])
@jwt_required()
def get_loan_offers():
    current_user_id = get_jwt_identity()
    offers = LoanOffer.query.filter_by(user_id=current_user_id).all()
    return jsonify([offer.to_dict() for offer in offers]), 200

@loans_bp.route("/active", methods=["GET"])
@jwt_required()
def get_active_loans():
    current_user_id = get_jwt_identity()
    # Empréstimos onde o usuário é devedor ou credor
    loans = Loan.query.filter(
        (Loan.debtor_id == current_user_id) | (Loan.creditor_id == current_user_id)
    ).all()
    return jsonify([loan.to_dict() for loan in loans]), 200



@loans_bp.route("/matches", methods=["GET"])
@jwt_required()
def get_loan_matches():
    current_user_id = get_jwt_identity()
    # Retorna matches onde o usuário é o solicitante ou o ofertante
    matches = LoanMatch.query.join(LoanRequest).join(LoanOffer).filter(
        (LoanRequest.user_id == current_user_id) | (LoanOffer.user_id == current_user_id)
    ).all()
    return jsonify([match.to_dict() for match in matches]), 200

