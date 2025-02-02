from sqlalchemy.orm import Session
from datetime import datetime
from app.models.notification import Notification
from app.services.email_services import send_email_notification

def check_and_create_stock_alert(stock_movement, db_session: Session):
  product = stock_movement.product 

  if product.quantity <= product.reorder_level:
    notification_type = "Low Stock Alert"
    message = f"Stock level for {product.name} (SKU: {product.sku}) is low."

    existing_notification = (
      db.session(Notification)
      .filter_by(product_id=product.id, type=notification_type)
      .first()
    )

    if existing_notification:
      return

    notification = Notification(
      type=notification_type,
      sent_at=datetime.utcnow(),
      product_id=product.id,
      user_id=product.user_id
    )
    
    db_session.add(notification)
    db_session.commit()

    user_email = product.user.email
    send_email_notification(user_email, message)

def check_all_products_and_notify(db_session, Session):
  from app.models.products import Products

  products = db_session.query(Products).all()
  for product in products:
    check_and_create_stock_alert(product, db_session)
