from flask import Flask
from .db import db, migrate, mail
import os
from flask_cors import CORS
from flask_login import LoginManager
from .models.user import User
from .routes.products_routes import bp as products_bp
from .routes.user_routes import bp as user_bp
from .routes.reports_routes import bp as report_bp
from .routes.notification_routes import bp as notification_bp
from .routes.auth_routes import bp as auth_bp
from .routes.stock_movement_routes import bp as stock_movement_bp

login_manager = LoginManager()

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    app.config['SECRET_KEY'] = 'b7f8a9c6d3e1f2g4h5i6j7k8l9m0n1o2'
    app.config["SESSION_TYPE"] = "filesystem"

    app.config['MAIL_SERVER'] = 'smtp.example.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@example.com'
    app.config['MAIL_PASSWORD'] = 'your-email-password'
    app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    allowed_origins = [
        "http://localhost:5173",  
        "https://ecocount-ims-backend.onrender.com"  
    ]
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": allowed_origins}})


    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"  
    login_manager.login_message = "Please log in to access this page."

    @login_manager.user_loader
    def load_user(user_id):
        print(f"🔹 Loading user from session: {user_id}") 
        return User.query.get(int(user_id))


    app.register_blueprint(products_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(stock_movement_bp)

    return app
