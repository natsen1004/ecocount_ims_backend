from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models.base import Base
from flask_socketio import SocketIO
from flask_cors import CORS

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
socketio = SocketIO()
cors = CORS()
