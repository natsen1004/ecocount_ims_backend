from flask import Blueprint, request, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from ..db import db

bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

@bp.post("/signup")
def signup_user():
    data = request.get_json()

    email = data.get("email", "").strip().lower()  
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

@bp.post("/login")
def login_user():
    data = request.get_json()
    email = data.get("email", "").strip().lower()  
    password = data.get("password", "")

    if not email or not password:
        print("Missing email or password")
        return {"error": "Email and password are required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        print(f"User with email {email} not found in DB")
        return {"error": "Invalid email or password"}, 401  

    print(f"Checking login for: {email}")
    print(f"Hashed Password in DB: {user.password_hash}")

    if not hasattr(user, "password_hash"):
        return {"error": "User password not set properly"}, 500  

    if not user.check_password(password):
        print("Password check failed")
        return {"error": "Invalid email or password"}, 401  

    print("Login successful!")
    return {"message": "Login successful", "user": user.to_dict()}, 200

