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
    product = Products.query.get(data.get("product_id"))
    user = User.query.get(data.get("user_id"))
    if not product or not user:
        abort(make_response({"error": "Product or user not found"}, 404))

    notification = Notification(
        type=data.get("type"),
        sent_at=datetime.utcnow(),
        product_id=product.id,
        user_id=user.id
    )
    db.session.add(notification)
    db.session.commit()
    return {"notification": notification.to_dict()}, 201

@bp.get("")
def get_notifications(user_id):
    user_id = request.args.get("user_id")
    if not user_id:
        response = ({"error": "User ID is required"}), 400
        return response
    
    notifications = db.session.query(Notification).filter_by(user_id=user_id, status="unread").all()

    notification_list = [
        {"id": n.id, "message": n.message, "timestamp": n.sent_at}
        for n in notifications
    ]

    return notification_list, 200

@bp.post("/mark_read")
def mark_notification_as_read():
    data = request.get_json()
    notification_id = data.get("notification_id")

    if not notification_id:
        return {"error": "Notification ID is required"}, 400

    notification = db.session.query(Notification).filter_by(id=notification_id).first()

    if not notification:
        return {"error": "Notification not found"}, 404

    notification.read = True 
    db.session.commit()

    return {"message": "Notification marked as read", "notification_id": notification_id}, 200
