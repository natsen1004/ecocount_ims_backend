from flask import Blueprint, request, abort, make_response
from ..models.user import User
from ..db import db
from datetime import datetime

bp = Blueprint("user_bp", __name__, url_prefix="/users")

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

    return {"user": user.to_dict()}, 200

@bp.put("/<user_id>")
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(make_response({"error": "User not found"}, 404))

    data = request.get_json()
    user.email = data.get("email", user.email)
    if data.get("password"):
        user.password = data["password"]  
    user.role = data.get("role", user.role)

    db.session.commit()
    return {"message": "User updated successfully", "user": user.to_dict()}, 200

@bp.delete("/<user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(make_response({"error": "User not found"}, 404))

    db.session.delete(user)
    db.session.commit()
    return {"message": f"User {user.email} deleted successfully!"}, 200

