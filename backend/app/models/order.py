from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    total_price = Column(Float, nullable=False, default=0.0)
    status = Column(String, default="PENDING")  # e.g. PENDING, PAID, SHIPPED

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 🔥 Relationship to many items
    cart_items = relationship("CartItem", back_populates="order", cascade="all, delete-orphan")