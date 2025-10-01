
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.kyc_service import KYCService

kyc_bp = Blueprint("kyc", __name__)
kyc_service = KYCService() # Instancia o serviço KYC

@kyc_bp.route("/upload_document", methods=["POST"])
@jwt_required()
def upload_document():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    document_type = data.get("document_type")
    document_url = data.get("document_url")

    if not all([document_type, document_url]):
        return jsonify({"message": "Tipo e URL do documento são obrigatórios"}), 400

    document, message = kyc_service.upload_document(current_user_id, document_type, document_url)
    if document:
        return jsonify({"message": message, "document": document.to_dict()}), 200
    return jsonify({"message": message}), 400

@kyc_bp.route("/status", methods=["GET"])
@jwt_required()
def get_kyc_status():
    current_user_id = get_jwt_identity()
    status, message = kyc_service.get_user_kyc_status(current_user_id)
    if status:
        return jsonify(status), 200
    return jsonify({"message": message}), 404

