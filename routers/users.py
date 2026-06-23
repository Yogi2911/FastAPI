from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from models.models import User
from schemas.schemas import UserOut
from utils.auth import get_current_user, get_admin_user
from typing import List

router = APIRouter()

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    return db.query(User).all()
