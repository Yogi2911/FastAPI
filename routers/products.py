from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database.db import get_db
from models.models import Product, Category, User
from schemas.schemas import ProductCreate, ProductUpdate, ProductOut, CategoryCreate, CategoryOut
from utils.auth import get_current_user, get_admin_user

router = APIRouter()

# ── Categories ────────────────────────────────────────────────────────────────

@router.post("/categories", response_model=CategoryOut, status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    if db.query(Category).filter(Category.name == payload.name).first():
        raise HTTPException(400, "Category already exists")
    cat = Category(name=payload.name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.get("/categories", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# ── Products ──────────────────────────────────────────────────────────────────

@router.post("/", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=List[ProductOut])
def list_products(
    db:          Session          = Depends(get_db),
    search:      Optional[str]   = Query(None, description="Search by product name"),
    category_id: Optional[int]   = Query(None, description="Filter by category"),
    min_price:   Optional[float] = Query(None),
    max_price:   Optional[float] = Query(None),
    in_stock:    bool             = Query(False),
    skip:        int              = Query(0, ge=0),
    limit:       int              = Query(20, le=100),
):
    q = db.query(Product).filter(Product.is_active == True)
    if search:
        q = q.filter(Product.name.ilike(f"%{search}%"))
    if category_id:
        q = q.filter(Product.category_id == category_id)
    if min_price is not None:
        q = q.filter(Product.price >= min_price)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)
    if in_stock:
        q = q.filter(Product.stock > 0)
    return q.offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(404, "Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    product.is_active = False  # Soft delete
    db.commit()
