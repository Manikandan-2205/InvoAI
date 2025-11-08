from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, PasswordUpdate
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

    def hash_password(password: str) -> str:
        sha256_hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return pwd_context.hash(sha256_hashed)

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        sha256_hashed = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return pwd_context.verify(sha256_hashed, hashed_password)


    def get_all_users(self):
        try:
            users = self.repo.get_all()
            logger.success(f"Fetched {len(users)} active users.")
            return Result.Ok(users, message="Users fetched successfully")
        except SQLAlchemyError:
            logger.exception("Error fetching users.")
            return Result.Fail("Database error while fetching users", code=500)

    def get_user_by_id(self, user_id: int):
        logger.info(f"Fetching user ID {user_id}")
        user = self.repo.get_by_id(user_id)
        if not user:
            logger.warning(f"User {user_id} not found.")
            return Result.Fail("User not found", code=404)
        logger.success(f"User {user_id} fetched successfully.")
        return Result.Ok(user, message="User fetched successfully")

    def create_user(self, data: UserCreate):
        try:
            user = User(
                bio_id=data.bio_id,
                user_name=data.user_name,
                password_hash=hash_password(data.password),  # bcrypt encrypted here ✅
                created_by=data.created_by,
                created_at=datetime.now(),
            )
            created = self.repo.create(user)
            return Result.Ok(created, message="User created successfully", code=201)
        except Exception as e:
            self.repo.rollback()
            logger.exception("Error creating user")
            return Result.Fail(str(e), code=500)

    def update_user(self, user_id: int, data: UserUpdate):
        existing = self.get_user_by_id(user_id)
        if not existing.success:
            return existing
        try:
            user = existing.data
            user.user_name = data.user_name
            user.bio_id = data.bio_id
            user.updated_by = data.updated_by
            user.updated_at = datetime.now()
            updated = self.repo.update(user)
            logger.success(f"User {user_id} updated successfully.")
            return Result.Ok(updated, message="User updated successfully")
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Database error while updating user.")
            return Result.Fail("Database error while updating user", code=500)

    def update_password(self, user_id: int, data: PasswordUpdate):
        existing = self.get_user_by_id(user_id)
        if not existing.success:
            return existing
        try:
            user = existing.data
            user.password_hash = self._hash_password(data.password)
            user.updated_by = data.updated_by
            user.updated_at = datetime.now()
            updated = self.repo.update(user)
            logger.success(f"Password updated successfully for user {user_id}")
            return Result.Ok(updated, message="Password updated successfully")
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error updating password.")
            return Result.Fail("Database error while updating password", code=500)

    def soft_delete_user(self, user_id: int):
        existing = self.get_user_by_id(user_id)
        if not existing.success:
            return existing
        try:
            user = existing.data
            user.is_deleted = 1
            user.updated_at = datetime.now()
            self.repo.update(user)
            logger.success(f"User {user_id} soft-deleted successfully.")
            return Result.Ok(user, message="User deleted successfully")
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error deleting user.")
            return Result.Fail("Database error while deleting user", code=500)
