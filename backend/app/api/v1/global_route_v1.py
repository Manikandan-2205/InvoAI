from fastapi import APIRouter, Depends
from app.core.database import get_db
from sqlalchemy.orm import Session

from backend.app.services import global_service

router = APIRouter()

def get_auth_service(db: Session = Depends(get_db)) -> global_service:
    repo = global_service(db)
    return AuthService(repo)