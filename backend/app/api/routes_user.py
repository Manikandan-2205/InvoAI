from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, get_db
from app.models.user_model import User

router = APIRouter()

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).filter(User.is_deleted == 0).all()
