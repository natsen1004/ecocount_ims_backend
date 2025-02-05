from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, String
from ..db import db
from typing import List


class Products(db.Model):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    sku: Mapped[str] = mapped_column(String, nullable=False)  
    quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    reorder_level: Mapped[int] = mapped_column(nullable=False, default=0)
    price: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=2), nullable=False, default=0.0)


    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="product", cascade="all, delete-orphan")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="products")
    reports: Mapped[List["Reports"]] = relationship("Reports", back_populates="product", cascade="all, delete-orphan")
    stock_movements: Mapped[List["StockMovement"]] = relationship("StockMovement", back_populates="product", cascade="all, delete-orphan")  
    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            sku=self.sku,
            quantity=self.quantity,
            reorder_level=self.reorder_level,
            price=float(self.price),
            user_id=self.user_id
        )

    @classmethod
    def from_dict(cls, products_data, user_id):
        return cls(
            name=products_data["name"],
            sku=products_data.get("sku", ""),
            quantity=products_data.get("quantity", 0),
            reorder_level=products_data.get("reorder_level", 0),
            price=products_data.get("price", 0.0),
            user_id=user_id 
        )

