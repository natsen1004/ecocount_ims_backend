from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import db
from typing import List

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)  
    role: Mapped[str] = mapped_column(nullable=False)

    products: Mapped[List["Products"]] = relationship("Products", back_populates="user")  
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user")  
    reports: Mapped[List["Reports"]] = relationship("Reports", back_populates="user")  

    @property
    def password(self):
        raise AttributeError("Password is not readable")
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = generate_password_hash(plain_text_password) 
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 
    
    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            role=self.role,
        )

    @classmethod
    def from_dict(cls, user_data):
        user = cls(
            email=user_data["email"],
            role=user_data["role"],
        )
        user.password = user_data["password"]  

        return user
