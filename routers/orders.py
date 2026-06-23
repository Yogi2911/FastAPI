from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from models.models import Order, OrderItem, CartItem, Product, User
from schemas.schemas import OrderCreate, OrderOut, OrderStatusUpdate
from utils.auth import get_current_user, get_admin_user

router = APIRouter()

@router.post("/checkout", response_model=OrderOut, status_code=201)
def checkout(payload: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(400, "Cart is empty")

    # Validate stock and calculate total
    total = 0.0
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product.stock < item.quantity:
            raise HTTPException(400, f"Insufficient stock for '{product.name}'")
        total += product.price * item.quantity

    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=round(total, 2),
        shipping_address=payload.shipping_address
    )
    db.add(order)
    db.flush()  # Get order.id before creating items

    # Create order items and deduct stock
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )
        product.stock -= item.quantity
        db.add(order_item)

    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=List[OrderOut])
def my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    return order

# Admin routes
@router.get("/admin/all", response_model=List[OrderOut])
def all_orders(db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    return db.query(Order).order_by(Order.created_at.desc()).all()

@router.put("/admin/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    order.status = payload.status
    db.commit()
    db.refresh(order)
    return order
