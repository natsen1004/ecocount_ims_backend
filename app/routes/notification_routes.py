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

    product_id = data.get("product_id")
    product = Products.query.get(product_id)
    if not product:
        abort(make_response({"error": "Product not found"}, 404))

    user_id = data.get("user_id")
    user = User.query.get(user_id)
    if not user:
        abort(make_response({"error": "User not found"}, 404))

    notification = Notification(
        type=data.get("type"),
        sent_at=datetime.utcnow(),
        product_id=product_id,
        user_id=user_id
    )

    db.session.add(notification)
    db.session.commit()
    
    from app.sockets import emit_notification
    emit_notification(user_id, product.name, notification.type)

    response = {"notification": notification.to_dict()}
    return response, 201

@bp.get("/<user_id>")
def get_notifications(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(make_response({"error": "User not found"}, 404))

    notifications = Notification.query.filter_by(user_id=user_id).all()
    return [notification.to_dict() for notification in notifications]

@bp.put("/<notification_id>/mark-as-read")
def mark_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        abort(make_response({"error": "Notification not found"}, 404))

    notification.sent_at = datetime.utcnow()
    db.session.commit()

    return {"message": "Notification marked as read"}, 200

@bp.delete("/<notification_id>")
def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        abort(make_response({"error": "Notification not found"}, 404))

    db.session.delete(notification)
    db.session.commit()

    return {"message": "Notification deleted successfully."}, 200
