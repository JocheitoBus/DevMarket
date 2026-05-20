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