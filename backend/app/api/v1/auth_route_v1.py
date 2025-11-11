from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.schemas.auth_schema import LoginRequest
from app.core.database import get_db
from app.utils.api_response import ApiResponse
from app.core.logger import logger
from app.repositories.auth_repository import AuthRepository

router = APIRouter()

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = AuthRepository(db)
    return AuthService(repo)

@router.post("/login", summary="User login")
async def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        result = await service.login(payload)
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception("Login error.")
        return ApiResponse.error(str(e), 500)
