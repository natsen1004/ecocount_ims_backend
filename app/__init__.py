from flask import Flask
from .db import db, migrate, cors, socketio
import os
from .routes.products_routes import bp as products_bp
from .routes.user_routes import bp as user_bp
from .routes.reports_routes import bp as report_bp
from .routes.notification_routes import bp as notification_bp
from .routes.auth_routes import bp as auth_bp

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": "*",  
                "supports_credentials": True,
            }
        },
    )

    socketio.init_app(
        app,
        cors_allowed_origins="*",  
        transports=["websocket", "polling"],  
    )

    app.register_blueprint(products_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(auth_bp)

    return app
