from sqlalchemy.exc import SQLAlchemyError
from app.models.user_model import User
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger
from app.core.result import Result


class UserRepository(BaseRepository):
    """
    Handles all database-level operations for User entity.
    Logging is limited to exceptions for cleaner output.
    """

    async def get_all(self) -> Result:
        try:
            users = self.db.query(User).filter(User.is_deleted == 0).all()
            return Result.Ok(data=users)
        except SQLAlchemyError:
            logger.exception("Database error while fetching all users.")
            return Result.Fail("Database error while fetching users", code=500)

    async def get_by_id(self, user_id: int) -> Result:
        try:
            user = self.db.query(User).filter(
                User.user_id == user_id, User.is_deleted == 0).first()
            
            if not user:
                return Result.Fail(message=f"User with ID {user_id} not found", code=404)
            return Result.Ok(data=user)
        except SQLAlchemyError:
            logger.exception(f"Database error while fetching user {user_id}.")
            return Result.Fail("Database error while fetching user", code=500)

    async def get_by_bio_id(self, bio_id: int) -> Result:
        try:
            users = self.db.query(User).filter(
                User.bio_id == bio_id, User.is_deleted == 0).all()
            
            if not users:
                return Result.Fail(f"No users found with bio ID {bio_id}", code=404)
            return Result.Ok(data=users)
        except SQLAlchemyError:
            logger.exception(f"Database error while fetching users by bio ID {bio_id}.")
            return Result.Fail("Database error while fetching users", code=500)

    async def create(self, user: User) -> Result:
        try:
            self.add(user)
            self.commit()
            self.refresh(user)
            return Result.Ok(data=user)
        except SQLAlchemyError:
            self.rollback()
            logger.exception(f"Database error while creating user '{user.user_name}'.")
            return Result.Fail("Database error while creating user", code=500)

    async def update(self, user: User) -> Result:
        try:
            self.commit()
            self.refresh(user)
            return Result.Ok(data=user)
        except SQLAlchemyError:
            self.rollback()
            logger.exception(f"Database error while updating user {user.user_id}.")
            return Result.Fail("Database error while updating user", code=500)
