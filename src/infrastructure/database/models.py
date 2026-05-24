from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime, timezone
from src.infrastructure.database.database import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    products = relationship("ProductModel", back_populates="owner", cascade="all, delete-orphan")

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), unique=True, nullable=False)
    price = Column(Float, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("UserModel", back_populates="products")

class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    price_at_purchase = Column(Float, nullable=False) 
    quantity = Column(Integer, default=1, nullable=False)

    product = relationship("ProductModel")

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, default=0.0, nullable=False)
    status = Column(String(50), default="pending", nullable=False) # pending, completed, cancelled
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    buyer = relationship("UserModel")
    items = relationship("OrderItemModel", backref="order", cascade="all, delete-orphan")