from sqlalchemy.orm import Session
from ..db import db
from datetime import datetime
from app.models.notification import Notification
from app.services.email_services import send_email_notification

def send_notification(user_id, message, db_session: Session, notification_type="General Alert", product_id=None):
    notification = Notification(
        type=notification_type,
        message=message,
        sent_at=datetime.utcnow(),
        user_id=user_id,
        product_id=product_id
    )

    db_session.add(notification)
    db_session.commit()
    print(f"Notification sent to user {user_id}: {message}")


def check_and_create_stock_alert(stock_movement, db_session: Session):
    """Checks stock level, logs stock movement, and sends notifications for low stock alerts."""
    product = stock_movement.product
    quantity_change = stock_movement.quantity_change

    movement_message = f"Stock updated: {product.name} (SKU: {product.sku}), changed by {quantity_change} units."
    send_notification(product.user_id, movement_message, db_session, "Stock Movement", product.id)

    if product.quantity <= product.reorder_level:
        low_stock_message = f"Low stock alert: {product.name} (SKU: {product.sku}). Only {product.quantity} left."

        existing_notification = db_session.query(Notification).filter_by(
            product_id=product.id, type="Low Stock Alert"
        ).first()

        if not existing_notification:
            send_notification(product.user_id, low_stock_message, db_session, "Low Stock Alert", product.id)

            notification = Notification(
                type="Low Stock Alert",
                message=low_stock_message,
                sent_at=datetime.utcnow(),
                product_id=product.id,
                user_id=product.user_id
            )
            db_session.add(notification)
            db_session.commit()

            user_email = product.user.email
            send_email_notification(user_email, low_stock_message)


def check_all_products_and_notify(db_session: Session):
    from app.models.products import Products

    products = db_session.query(Products).all()
    for product in products:
        class StockMovement:
            def __init__(self, product):
                self.product = product
                self.quantity_change = 0 
        check_and_create_stock_alert(StockMovement(product), db_session)
