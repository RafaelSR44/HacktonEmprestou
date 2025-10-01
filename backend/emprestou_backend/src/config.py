
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-segura'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/ubuntu/emprestou/backend/emprestou_backend/app.db?foreign_keys=on'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-jwt-key'
    
    # Configurações do WhatsApp Bot
    WHATSAPP_API_URL = os.environ.get('WHATSAPP_API_URL') or 'http://localhost:5001/whatsapp'
    WHATSAPP_API_TOKEN = os.environ.get('WHATSAPP_API_TOKEN') or 'whatsapp-api-token'

    # Configurações de serviços mock
    KYC_SERVICE_URL = os.environ.get('KYC_SERVICE_URL') or 'http://localhost:5002/kyc'
    SCORE_SERVICE_URL = os.environ.get('SCORE_SERVICE_URL') or 'http://localhost:5003/score'
    PAYMENT_SERVICE_URL = os.environ.get('PAYMENT_SERVICE_URL') or 'http://localhost:5004/payment'

