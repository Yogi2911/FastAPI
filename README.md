# 🛒 E-Commerce FastAPI Backend

A production-ready REST API for an e-commerce platform built with **FastAPI + SQLAlchemy + JWT Auth**.

---

## 📁 Project Structure

```
ecommerce/
├── main.py                  # App entry point & router registration
├── requirements.txt
├── database/
│   └── db.py               # SQLAlchemy engine, session, Base
├── models/
│   └── models.py           # DB models: User, Product, Category, Cart, Order
├── schemas/
│   └── schemas.py          # Pydantic request/response schemas
├── routers/
│   ├── auth.py             # Register, Login
│   ├── users.py            # Profile, Admin user list
│   ├── products.py         # Products CRUD + Category CRUD
│   ├── cart.py             # Cart management
│   └── orders.py           # Checkout, order tracking
└── utils/
    └── auth.py             # JWT helpers, password hashing, guards
```

---

## ⚡ Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
uvicorn main:app --reload

# 3. Open interactive API docs
http://localhost:8000/docs
```

---

## 🔐 Authentication

JWT Bearer token — include in headers:
```
Authorization: Bearer <your_token>
```

---

## 📡 API Endpoints

### Auth
| Method | Endpoint              | Description         |
|--------|-----------------------|---------------------|
| POST   | /api/auth/register    | Register new user   |
| POST   | /api/auth/login       | Login & get token   |

### Users
| Method | Endpoint              | Auth     | Description         |
|--------|-----------------------|----------|---------------------|
| GET    | /api/users/me         | User     | Get own profile     |
| GET    | /api/users/           | Admin    | List all users      |

### Products
| Method | Endpoint                    | Auth     | Description                  |
|--------|-----------------------------|----------|------------------------------|
| GET    | /api/products/              | Public   | List/search/filter products  |
| GET    | /api/products/{id}          | Public   | Get single product           |
| POST   | /api/products/              | Admin    | Create product               |
| PUT    | /api/products/{id}          | Admin    | Update product               |
| DELETE | /api/products/{id}          | Admin    | Soft-delete product          |
| GET    | /api/products/categories    | Public   | List categories              |
| POST   | /api/products/categories    | Admin    | Create category              |

**Product Query Params:**
- `search` — name keyword
- `category_id` — filter by category
- `min_price` / `max_price` — price range
- `in_stock=true` — only in-stock items
- `skip` / `limit` — pagination

### Cart
| Method | Endpoint              | Auth  | Description              |
|--------|-----------------------|-------|--------------------------|
| GET    | /api/cart/            | User  | View cart + total price  |
| POST   | /api/cart/            | User  | Add item to cart         |
| PUT    | /api/cart/{item_id}   | User  | Update quantity          |
| DELETE | /api/cart/{item_id}   | User  | Remove item              |
| DELETE | /api/cart/            | User  | Clear entire cart        |

### Orders
| Method | Endpoint                        | Auth   | Description             |
|--------|---------------------------------|--------|-------------------------|
| POST   | /api/orders/checkout            | User   | Place order from cart   |
| GET    | /api/orders/                    | User   | My order history        |
| GET    | /api/orders/{id}                | User   | Get specific order      |
| GET    | /api/orders/admin/all           | Admin  | All orders (admin)      |
| PUT    | /api/orders/admin/{id}/status   | Admin  | Update order status     |

**Order Statuses:** `pending` → `confirmed` → `shipped` → `delivered` / `cancelled`

---

## 🗄️ Switch to PostgreSQL

In `database/db.py`, replace the DATABASE_URL:
```python
DATABASE_URL = "postgresql://user:password@localhost/ecommerce_db"
```

And remove `connect_args={"check_same_thread": False}`.

---

## 🔒 Production Checklist

- [ ] Move `SECRET_KEY` to environment variable (`os.getenv("SECRET_KEY")`)
- [ ] Set `allow_origins` to your actual frontend URL in CORS middleware
- [ ] Switch SQLite → PostgreSQL
- [ ] Add rate limiting (e.g. `slowapi`)
- [ ] Add payment gateway integration (Razorpay / Stripe)
- [ ] Add email notifications on order placement
