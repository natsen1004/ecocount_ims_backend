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

@bp.get("/<user_id>")
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return [notification.to_dict() for notification in notifications], 200

