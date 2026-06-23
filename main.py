from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine, Base
from routers import auth, products, cart, orders, users

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce API",
    description="Full-featured e-commerce REST API built with FastAPI",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router,     prefix="/api/auth",     tags=["Auth"])
app.include_router(users.router,    prefix="/api/users",    tags=["Users"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(cart.router,     prefix="/api/cart",     tags=["Cart"])
app.include_router(orders.router,   prefix="/api/orders",   tags=["Orders"])

@app.get("/")
def root():
    return {"message": "E-Commerce API is running!", "docs": "/docs"}
