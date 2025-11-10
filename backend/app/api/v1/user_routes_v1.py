from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, PasswordUpdate
from app.core.database import get_db
from app.utils.api_response import ApiResponse
from app.core.logger import logger
from app.repositories.user_repository import UserRepository

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency to inject UserService."""
    repo = UserRepository(db)
    return UserService(repo)


@router.get("/", summary="Get all users")
async def get_all_users(service: UserService = Depends(get_user_service)):
    try:
        result =await service.get_all_users()
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception("Error fetching users.")
        return ApiResponse.error(str(e), 500)


@router.get("/{user_id}", summary="Get user by ID")
async def get_user_by_id(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        result =await service.get_user_by_id(user_id)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception(f"Error fetching user {user_id}")
        return ApiResponse.error(str(e), 500)


@router.get("/bio/{bio_id}", summary="Get users by Bio ID")
async def get_user_by_bio_id(bio_id: int, service: UserService = Depends(get_user_service)):
    """
    Returns a list of all users with the given Bio ID.
    """
    try:
        result =await service.get_user_by_bio_id(bio_id)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception(f"Error fetching user(s) by bio_id {bio_id}")
        return ApiResponse.error(str(e), 500)


@router.post("/", summary="Create new user", status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        result =await service.create_user(payload)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception("Error creating user.")
        return ApiResponse.error(str(e), 500)


@router.put("/{user_id}", summary="Update existing user")
async def update_user(user_id: int, payload: UserUpdate, service: UserService = Depends(get_user_service)):
    try:
        result =await service.update_user(user_id, payload)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception(f"Error updating user {user_id}")
        return ApiResponse.error(str(e), 500)


@router.patch("/{user_id}/password", summary="Update user password")
async def update_password(user_id: int, payload: PasswordUpdate, service: UserService = Depends(get_user_service)):
    try:
        result = service.update_password(user_id, payload)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception(f"Error updating password for user {user_id}")
        return ApiResponse.error(str(e), 500)


@router.delete("/{user_id}", summary="Soft delete user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        result = service.soft_delete_user(user_id)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception(f"Error deleting user {user_id}")
        return ApiResponse.error(str(e), 500)
