from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from datetime import datetime

class Notification(db.Model):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str]
    sent_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.utcnow)

    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("products.id"))
    product = relationship("Products", back_populates="notifications")

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["User"]] = relationship("User", back_populates="notifications")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "sent_at": self.sent_at,
        }

    @classmethod
    def from_dict(cls, notification_data):
        return cls(
            type=notification_data["type"],
            sent_at=notification_data.get("sent_at", datetime.utcnow()),
            product_id=notification_data.get("product_id", None),
            user_id=notification_data.get("user_id", None),
        )
