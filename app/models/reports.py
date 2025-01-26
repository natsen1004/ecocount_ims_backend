from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from ..db import db
from typing import Optional
from datetime import datetime
from ..models.products import Products
from ..models.user import User

class Reports(db.Model):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity_sold: Mapped[int] = mapped_column(nullable=False, default=0)
    stock_movement: Mapped[int] = mapped_column(nullable=False, default=0)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("products.id"))
    product: Mapped[Optional["Products"]] = relationship("Products", back_populates="reports")

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship(back_populates="reports")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "quantity_sold": self.quantity_sold,
            "stock_movement": self.stock_movement,
            "created_on": self.created_on.strftime("%M-%d-%y %H:%M:%S")
        }