from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import CartItem, Product, User
from schemas.schemas import CartItemAdd, CartItemUpdate, CartOut
from utils.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=CartOut)
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    total = sum(item.product.price * item.quantity for item in items)
    return {"items": items, "total_price": round(total, 2)}

@router.post("/", status_code=201)
def add_to_cart(payload: CartItemAdd, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == payload.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(404, "Product not found")
    if product.stock < payload.quantity:
        raise HTTPException(400, f"Only {product.stock} units in stock")

    existing = db.query(CartItem).filter(
        CartItem.user_id == current_user.id,
        CartItem.product_id == payload.product_id
    ).first()

    if existing:
        existing.quantity += payload.quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=payload.product_id, quantity=payload.quantity)
        db.add(cart_item)
    db.commit()
    return {"message": "Item added to cart"}

@router.put("/{item_id}")
def update_cart_item(item_id: int, payload: CartItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not item:
        raise HTTPException(404, "Cart item not found")
    if payload.quantity <= 0:
        db.delete(item)
    else:
        item.quantity = payload.quantity
    db.commit()
    return {"message": "Cart updated"}

@router.delete("/{item_id}", status_code=204)
def remove_from_cart(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not item:
        raise HTTPException(404, "Cart item not found")
    db.delete(item)
    db.commit()

@router.delete("/", status_code=204)
def clear_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
