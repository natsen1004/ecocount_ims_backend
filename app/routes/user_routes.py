from flask import Blueprint, request, Response, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from ..db import db
from datetime import datetime

bp = Blueprint("user_bp", __name__, url_prefix="/users")

@bp.post("")
def create_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    role = data.get("role", "user")

    if not email or not password or not name:
        abort(make_response({"error": "Missing required fields"}, 400))

    if User.query.filter_by(email=email).first():
        abort(make_response({"error": "Email already exist"}, 409))

    password_hash = generate_password_hash(password)

    new_user = User(
        email=email,
        password=password_hash,
        name=name,
        role=role,
    )

    db.session.add(new_user)
    db.session.commit()

    response = {"user": new_user.to_dict()}

    return response, 201

# Authenticate users
@bp.post("")
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        abort(make_response({"error": "Invalid email or password"}, 401))

    return {"user": user.to_dict()}, 200

@bp.get("")
def get_users():
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return users_list, 200

@bp.get("/<user_id>")
def get_one_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(make_response({"error": "User not found"}, 404))

    response = {"user": user.to_dict()}
    return response, 200

@bp.put("")
def upate_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(make_response({"error": "User not found"}, 404))

    data = request.get_json()

    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)

    if data.get("password"):
        user.password_hash = generate_password_hash(data["password"])
    user.role = data.get("role", user.role)
    user.updated_at = datetime.utcnow()

    db.session.commit()
    response = {"user": user.to_dict()}

    return response, 200

@bp.delete("")
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(make_response({"error": "User not found"}, 404))

    db.session.delete(user)
    db.session.commit()

    response = {"message": f"User {user.name} deleted successfully!"}

    return response, 200
