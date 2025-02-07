from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, String
from ..db import db 
from datetime import datetime
from typing import Optional

class StockMovement(db.Model):
  __tablename__ = "stock_movements"
  __table_args__ = {'extend_existing': True}

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  sku: Mapped[str] = mapped_column(String, nullable=False) 
  quantity_change: Mapped[int] = mapped_column(nullable=False)
  new_quantity: Mapped[int] = mapped_column(nullable=False)
  timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)  
  reason: Mapped[str] = mapped_column(String, nullable=True)  

  product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
  product: Mapped["Products"] = relationship("Products", back_populates="stock_movements") 

  report_id: Mapped[Optional[int]] = mapped_column(ForeignKey("reports.id"))
  report: Mapped[Optional["Reports"]] = relationship("Reports", back_populates="stock_movements") 

  user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
  user: Mapped["User"] = relationship("User", back_populates="stock_movements") 
  
  def to_dict(self):
    return dict(
      id=self.id,
      sku=self.sku,
      product_id=self.product_id,
      user_id=self.user_id,
      quantity_change=self.quantity_change,
      new_quantity=self.new_quantity,
      timestamp=self.timestamp,
      reason=self.reason,
      report_id=self.report_id
    )


  @classmethod
  def from_dict(cls, stock_movement_data):
    timestamp_str = stock_movement_data.get("timestamp")
    if timestamp_str:
      try:
          timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00.00"))
      except (TypeError, ValueError):
        timestamp = datetime.utcnow()
    else:
      timestamp = datetime.utcnow()

    return cls (
      product_id=stock_movement_data["product_id"],
      user_id=stock_movement_data["user_id"],
      sku=stock_movement_data["sku"],
      quantity_change=stock_movement_data["quantity_change"],
      new_quantity=stock_movement_data["new_quantity"],
      timestamp=timestamp,
      reason=stock_movement_data.get("reason"),
      report_id=stock_movement_data.get("report_id") 
    )  
  
