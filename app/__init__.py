from flask import Flask
from .db import db, migrate, mail
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .routes.products_routes import bp as products_bp
from .routes.user_routes import bp as user_bp
from .routes.reports_routes import bp as report_bp
from .routes.notification_routes import bp as notification_bp
from .routes.auth_routes import bp as auth_bp
from .routes.stock_movement_routes import bp as stock_movement_bp

load_dotenv() 

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    app.config['MAIL_SERVER'] = 'smtp.example.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@example.com'
    app.config['MAIL_PASSWORD'] = 'your-email-password'
    app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "fallback_secret_key")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]  
    app.config["JWT_HEADER_NAME"] = "Authorization" 
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    print("🔹 Loading JWT Configuration...")
    print(f"Render Environment - JWT_SECRET_KEY: {os.environ.get('JWT_SECRET_KEY')}")
    print(f"JWT_SECRET_KEY: {app.config['JWT_SECRET_KEY']}")
    print(f"JWT_TOKEN_LOCATION: {app.config['JWT_TOKEN_LOCATION']}")
    print(f"JWT_HEADER_NAME: {app.config['JWT_HEADER_NAME']}")
    print(f"JWT_HEADER_TYPE: {app.config['JWT_HEADER_TYPE']}")

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    allowed_origins = [
        "http://localhost:5173",  
        "https://your-frontend-app.onrender.com"  
    ]
    print(f"🔹 CORS allowed origins: {allowed_origins}")
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://your-frontend.onrender.com"], "supports_credentials": True}})
    jwt = JWTManager(app) 

    app.register_blueprint(products_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_movement_bp)

    return app
