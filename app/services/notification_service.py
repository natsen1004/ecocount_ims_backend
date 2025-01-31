from sqlalchemy.orm import Session
from datetime import datetime
from app.models.products import Products
from app.models.notification import Notification

def check_and_create_stock_alert(stock_movement, db_session: Session):
  product = stock_movement.product 

  if product.quantity <= product.reorder_level:
    notification_type = "Low Stock Alert"
    message = f"Stock level for {product.name} (SKU: {product.sku}) is low."

    notification = Notification(
      type=notification_type,
      sent_at=datetime.utcnow(),
      product_id=product.id,
      user_id=product.user_id
    )
    
    db_session.add(notification)
    db_session.commit()

    