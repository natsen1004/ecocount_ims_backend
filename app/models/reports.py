from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from ..db import db
from typing import Optional, List
from datetime import datetime
from ..models.products import Products
from ..models.user import User
from ..models.stock_movement import StockMovement

class Reports(db.Model):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity_sold: Mapped[int] = mapped_column(nullable=False, default=0)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    product: Mapped[Optional["Products"]] = relationship("Products", back_populates="reports")

    user: Mapped[Optional["User"]] = relationship("User", back_populates="reports")
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    stock_movements: Mapped[List["StockMovement"]] = relationship("StockMovement", back_populates="report", cascade="all, delete-orphan")  

    def to_dict(self):
        return dict(
            id=self.id,
            product_id=self.product_id,
            quantity_sold=self.quantity_sold,
            created_on=self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            user_id=self.user_id,
            stock_movements=[sm.to_dict() for sm in self.stock_movements] if self.stock_movements else []
        )
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data["product_id"],
            quantity_sold=data.get("quantity_sold", 0),
            user_id=data["user_id"]
        )

