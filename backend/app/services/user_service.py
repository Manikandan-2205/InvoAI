from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from app.models.user_model import User
from app.schemas.user_schema import (
    UserCreate,
    UserListResponse,
    UserUpdate,
    PasswordUpdate,
    UserResponse,
)
from app.core.result import Result
from app.core.logger import logger
from app.repositories.user_repository import UserRepository
import hashlib


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    Business logic layer for User operations.
    """

    def __init__(self, repo: UserRepository):
        self.repo = repo

    # 🔐 Password Utilities
    def hash_password(self, password: str) -> str:
        sha256_hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return pwd_context.hash(sha256_hashed)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        sha256_hashed = hashlib.sha256(
            plain_password.encode("utf-8")).hexdigest()
        return pwd_context.verify(sha256_hashed, hashed_password)

    async def get_all_users(self) -> Result:
        try:
            repo_result = await self.repo.get_all()

            if not repo_result.success:
                return repo_result

            user_list = [UserResponse.from_orm(u) for u in repo_result.data]
            response = UserListResponse(users=user_list, total=len(user_list))
            return Result.Ok(data=response.dict())
        except SQLAlchemyError:
            logger.exception("Error fetching users in service.")
            return Result.Fail("Error fetching users in service", code=500)

    async def get_user_by_id(self, user_id: int) -> Result:
        try:
            result = await self.repo.get_by_id(user_id)

            if not result.success or not result.data:
                return Result.Fail("User not found", code=404)

            user = result.data  # Unwrap the Result
            user_data = UserResponse.from_orm(user).dict()
            return Result.Ok(user_data, message="User fetched successfully", code=200)
        except SQLAlchemyError:
            logger.exception(f"Error fetching user {user_id}.")
            return Result.Fail("Database error while fetching user", code=500)

    async def get_user_by_bio_id(self, bio_id: int) -> Result:
        """
        Get all users matching a given Bio ID.
        """
        try:
            users = await self.repo.get_by_bio_id(bio_id)
            if not users:
                return Result.Fail("No users found for this Bio ID", code=404)

            # Convert list of ORM objects to list of dicts
            user_data = [UserResponse.from_orm(
                user).dict() for user in users.data]
            return Result.Ok(user_data, message="Users fetched successfully", code=200)

        except SQLAlchemyError:
            logger.exception(f"Error fetching users with Bio ID {bio_id}.")
            return Result.Fail("Database error while fetching users by bio_id", code=500)

    async def create_user(self, data: UserCreate) -> Result:
        try:
            hash_password = self.hash_password(data.password)

            user = User(
                bio_id=data.bio_id,
                user_name=data.user_name,
                password_hash=hash_password,
                created_by=data.created_by,
                created_at=datetime.now(),
            )
            created = await self.repo.create(user)
            user_data = UserResponse.from_orm(created.data).dict()
            return Result.Ok(user_data, message="User created successfully", code=201)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Database error while creating user.")
            return Result.Fail("Database error while creating user", code=500)
        except Exception as e:
            self.repo.rollback()
            logger.exception("Unexpected error while creating user.")
            return Result.Fail(str(e), code=500)

    async def update_user(self, user_id: int, data: UserUpdate) -> Result:
        res = await self.repo.get_by_id(user_id)
        if not res.success:
            return Result.Fail("User not found", code=404)

        try:
            existing = res.data

            existing.user_name = data.user_name
            existing.bio_id = data.bio_id
            existing.updated_by = data.updated_by
            existing.updated_at = datetime.now()

            updated = await self.repo.update(existing)
            user_data = UserResponse.from_orm(updated.data).dict()

            return Result.Ok(data=user_data, message="User updated successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error updating user.")
            return Result.Fail("Database error while updating user", code=500)

    async def update_password(self, user_id: int, data: PasswordUpdate) -> Result:
        res = await self.repo.get_by_id(user_id)

        if not res.success:
            return Result.Fail("User not found", code=404)

        try:
            new_password = self.hash_password(data.password)

            existing = res.data
            existing.password_hash = new_password
            existing.updated_by = data.updated_by
            existing.updated_at = datetime.now()

            # Ensure update is awaited if async
            updated = await self.repo.update(existing)

            if not updated.success:
                return Result.Fail("Failed to update password", code=500)

            return Result.Ok(message="Password updated successfully", code=200)
        except SQLAlchemyError as e:
            await self.repo.rollback()
            logger.exception(str(e))
            return Result.Fail("Database error while updating password", code=500)

    async def soft_delete_user(self, user_id: int) -> Result:
        res = await self.repo.get_by_id(user_id)

        if not res.success:
            return Result.Fail("User not found", code=404)

        try:
            existing = res.data
            existing.is_deleted = 1
            existing.updated_at = datetime.now()

            deleted = await self.repo.update(existing)
            if not deleted.success:
                    return Result.Fail("Failed to deleted password", code=500)

            return Result.Ok(message="User deleted successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error deleting user.")
            return Result.Fail("Database error while deleting user", code=500)
