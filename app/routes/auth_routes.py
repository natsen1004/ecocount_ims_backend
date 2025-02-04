from flask import Blueprint, request, abort, make_response
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
    from werkzeug.security import generate_password_hash 
    new_user.password_hash = generate_password_hash(password)  

    print(f"Stored Hashed Password: {new_user.password_hash}") 

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
    print(f"Attempting to check password: {password}")

    if not hasattr(user, "password_hash"):
        print("User has no password hash stored!")
        return {"error": "User password not set properly"}, 500  

    from werkzeug.security import check_password_hash
    is_match = check_password_hash(user.password_hash, password)

    print(f"Manual Password Check: {is_match}")  
    if not is_match:
        print("Password check failed! Incorrect password entered.")
        return {"error": "Invalid email or password"}, 401  

    print(f"Password match! Logging in {email}")

    return {"message": "Login successful", "user": user.to_dict()}, 200


