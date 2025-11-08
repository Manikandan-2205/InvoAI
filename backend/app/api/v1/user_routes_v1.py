from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, PasswordUpdate
from app.core.database import get_db
from app.utils.common_response import success_response, error_response
from app.core.logger import logger

# Router
router = APIRouter()

# Dependency Injection — Service layer per request
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


# ==========================
# CRUD ROUTES
# ==========================

@router.get("/", summary="Get all users")
def get_all_users(service: UserService = Depends(get_user_service)):
    """
    Fetch all active (non-deleted) users.
    """
    try:
        users = service.get_all_users()
        return success_response("Fetched all users successfully.", users)
    except Exception as e:
        logger.exception("Error fetching users.")
        return error_response(str(e))


@router.get("/{user_id}", summary="Get user by ID")
def get_user_by_id(user_id: int, service: UserService = Depends(get_user_service)):
    """
    Retrieve a single user by ID.
    """
    try:
        user = service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return success_response("Fetched user successfully.", user)
    except Exception as e:
        logger.exception(f"Error fetching user {user_id}")
        return error_response(str(e))


@router.post("/", summary="Create new user", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    """
    Create a new user entry.
    """
    try:
        new_user = service.create_user(payload)
        return success_response("User created successfully.", new_user)
    except Exception as e:
        logger.exception("Error creating user.")
        return error_response(str(e))


@router.put("/{user_id}", summary="Update existing user")
def update_user(user_id: int, payload: UserUpdate, service: UserService = Depends(get_user_service)):
    """
    Update an existing user record.
    """
    try:
        updated_user = service.update_user(user_id, payload)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return success_response("User updated successfully.", updated_user)
    except Exception as e:
        logger.exception(f"Error updating user {user_id}")
        return error_response(str(e))


@router.patch("/{user_id}/password", summary="Update user password")
def update_password(user_id: int, payload: PasswordUpdate, service: UserService = Depends(get_user_service)):
    """
    Update a user's password securely.
    """
    try:
        updated_user = service.update_password(user_id, payload)
        return success_response("Password updated successfully.", updated_user)
    except Exception as e:
        logger.exception(f"Error updating password for user {user_id}")
        return error_response(str(e))


@router.delete("/{user_id}", summary="Soft delete user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    """
    Soft delete user (mark as deleted).
    """
    try:
        service.delete_user(user_id)
        return success_response("User deleted successfully.")
    except Exception as e:
        logger.exception(f"Error deleting user {user_id}")
        return error_response(str(e))
