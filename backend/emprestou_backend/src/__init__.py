
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    from src.routes.auth import auth_bp
    from src.routes.users import users_bp
    from src.routes.loans import loans_bp
    from src.routes.accounts import accounts_bp
    from src.routes.kyc import kyc_bp
    from src.routes.bot import bot_bp
    from src.routes.credit_score import credit_score_bp
    from src.routes.payments import payments_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(loans_bp, url_prefix="/api/loans")
    app.register_blueprint(accounts_bp, url_prefix="/api/accounts")
    app.register_blueprint(kyc_bp, url_prefix="/api/kyc")
    app.register_blueprint(bot_bp, url_prefix="/api/bot")
    app.register_blueprint(credit_score_bp, url_prefix="/api/credit-score")
    app.register_blueprint(payments_bp, url_prefix="/api/payments")

    return app

