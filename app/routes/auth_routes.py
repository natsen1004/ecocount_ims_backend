from flask import Blueprint, request, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from ..db import db

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@auth_bp.post("/signup")
def signup_user():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")  

    if not email or not password:
        abort(make_response({"error": "Email and password are required"}, 400))

    if User.query.filter_by(email=email).first():
        abort(make_response({"error": "Email already exists"}, 409))

    new_user = User(
        email=email,
        role=role,
    )
    new_user.password = password  

    db.session.add(new_user)
    db.session.commit()

    return {"message": "User created successfully", "user": new_user.to_dict()}, 201

@auth_bp.post("/login")
def login_user():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        abort(make_response({"error": "Email and password are required"}, 400))

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):  
        abort(make_response({"error": "Invalid email or password"}, 401))

    return {"message": "Login successful", "user": user.to_dict()}, 200
