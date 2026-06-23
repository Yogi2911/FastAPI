from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime
import enum

class OrderStatus(str, enum.Enum):
    pending   = "pending"
    confirmed = "confirmed"
    shipped   = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    email      = Column(String, unique=True, index=True, nullable=False)
    password   = Column(String, nullable=False)
    is_admin   = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete")
    orders     = relationship("Order",    back_populates="user",  cascade="all, delete")


class Category(Base):
    __tablename__ = "categories"

    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String, unique=True, nullable=False)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False, index=True)
    description = Column(Text)
    price       = Column(Float, nullable=False)
    stock       = Column(Integer, default=0)
    image_url   = Column(String)
    is_active   = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at  = Column(DateTime, default=datetime.utcnow)

    category   = relationship("Category",  back_populates="products")
    cart_items = relationship("CartItem",  back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")


class CartItem(Base):
    __tablename__ = "cart_items"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity   = Column(Integer, default=1)

    user    = relationship("User",    back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


class Order(Base):
    __tablename__ = "orders"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"))
    total_amount    = Column(Float, nullable=False)
    status          = Column(Enum(OrderStatus), default=OrderStatus.pending)
    shipping_address = Column(Text, nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow)

    user        = relationship("User",      back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete")


class OrderItem(Base):
    __tablename__ = "order_items"

    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order   = relationship("Order",   back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
