from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user_model import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")

def get_users(db: Session = Depends(get_db)):
    return db.query(User).filter(User.is_deleted == 0).all()
