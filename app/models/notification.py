from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from datetime import datetime

class Notification(db.Model):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(default=lambda: datetime.utcnow())  
    read: Mapped[bool] = mapped_column(default=False)

    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("products.id"), nullable=True)  
    product = relationship("Products", back_populates="notifications") 

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="notifications")

    def to_dict(self):
        return dict(
            id=self.id,
            type=self.type,
            sent_at=self.sent_at.isoformat() if self.sent_at else None, 
            read=self.read,
            product_id=self.product_id,
            user_id=self.user_id
        )

    @classmethod
    def from_dict(cls, notification_data):
        return cls(
            type=notification_data.get("type"),
            sent_at=notification_data.get("sent_at", datetime.utcnow()),
            product_id=notification_data.get("product_id"),  
            user_id=notification_data.get("user_id"),  
        )
