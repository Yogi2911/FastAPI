from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models.models import OrderStatus

# ── Auth / User ──────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    name:     str
    email:    EmailStr
    password: str

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class UserOut(BaseModel):
    id:         int
    name:       str
    email:      str
    is_admin:   bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"

# ── Category ─────────────────────────────────────────────────────────────────

class CategoryCreate(BaseModel):
    name: str

class CategoryOut(BaseModel):
    id:   int
    name: str

    class Config:
        from_attributes = True

# ── Product ──────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name:        str
    description: Optional[str] = None
    price:       float
    stock:       int
    image_url:   Optional[str] = None
    category_id: Optional[int] = None

class ProductUpdate(BaseModel):
    name:        Optional[str]   = None
    description: Optional[str]   = None
    price:       Optional[float] = None
    stock:       Optional[int]   = None
    image_url:   Optional[str]   = None
    is_active:   Optional[bool]  = None
    category_id: Optional[int]   = None

class ProductOut(BaseModel):
    id:          int
    name:        str
    description: Optional[str]
    price:       float
    stock:       int
    image_url:   Optional[str]
    is_active:   bool
    category:    Optional[CategoryOut]
    created_at:  datetime

    class Config:
        from_attributes = True

# ── Cart ─────────────────────────────────────────────────────────────────────

class CartItemAdd(BaseModel):
    product_id: int
    quantity:   int = 1

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemOut(BaseModel):
    id:       int
    quantity: int
    product:  ProductOut

    class Config:
        from_attributes = True

class CartOut(BaseModel):
    items:       List[CartItemOut]
    total_price: float

# ── Order ─────────────────────────────────────────────────────────────────────

class OrderCreate(BaseModel):
    shipping_address: str

class OrderItemOut(BaseModel):
    id:         int
    quantity:   int
    unit_price: float
    product:    ProductOut

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id:               int
    total_amount:     float
    status:           OrderStatus
    shipping_address: str
    created_at:       datetime
    order_items:      List[OrderItemOut]

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
