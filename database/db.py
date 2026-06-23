from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite for local dev — swap with PostgreSQL for production:
# DATABASE_URL = "postgresql://user:password@localhost/ecommerce_db"
DATABASE_URL = "sqlite:///./ecommerce.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
