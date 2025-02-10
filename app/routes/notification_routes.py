from flask import Blueprint, request, abort, make_response
from ..models.notification import Notification 
from ..models.products import Products
from ..models.user import User
from ..db import db
from datetime import datetime

bp = Blueprint("notification_bp", __name__, url_prefix="/notifications")

@bp.post("")
def create_notification():
    data = request.get_json()
    user_email = data.get("user_email")
    product_name = data.get("product_name") 
    notification_type = data.get("type")
    message = data.get("message", "No message provided.")  

    if not user_email or not product_name or not notification_type:
        return make_response({"error": "Missing required fields"}, 400)

    user = User.query.filter_by(email=user_email).first()
    product = Products.query.filter_by(name=product_name).first()  
    if not product or not user:
        return make_response({"error": "Product or user not found"}, 404)

    try:
        notification = Notification(
            type=notification_type,
            message=message,
            sent_at=datetime.utcnow(),
            product_id=product.id,  
            user_id=user.id
        )

        db.session.add(notification)
        db.session.commit()

        return {"notification": notification.to_dict()}, 201

    except Exception as e:
        db.session.rollback()  
        return make_response({"error": f"Failed to create notification: {str(e)}"}, 500)



@bp.get("")
def get_notifications():
    user_email = request.args.get("user_email")

    if not user_email:
        return make_response({"error": "User email is required"}, 400)

    user = User.query.filter_by(email=user_email).first()
    
    if not user:
        return make_response({"error": "User not found"}, 404)

    notifications = Notification.query.filter_by(user_id=user.id).all()

    notification_list = [
        {
            "id": n.id,
            "type": n.type,
            "message": getattr(n, "message", "No message"), 
            "sent_at": n.sent_at.isoformat(),
            "read": n.read,
            "product_id": n.product_id,
            "user_id": n.user_id
        }
        for n in notifications
    ]

    return notification_list


@bp.post("/mark_read")
def mark_notification_as_read():
    data = request.get_json()
    notification_id = data.get("notification_id")
    user_email = data.get("user_email")

    if not notification_id or not user_email:
        return make_response({"error": "Notification ID and user email are required"}, 400)

    user = User.query.filter_by(email=user_email).first()

    if not user:
        return make_response({"error": "User not found"}, 404)

    notification = Notification.query.filter_by(id=notification_id, user_id=user.id).first()

    if not notification:
        return make_response({"error": "Notification not found or does not belong to this user"}, 404)

    notification.read = True
    db.session.commit()

    return {"message": "Notification marked as read", "notification_id": notification_id}, 200
