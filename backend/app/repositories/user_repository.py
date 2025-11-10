from sqlalchemy.exc import SQLAlchemyError
from app.models.user_model import User
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger


class UserRepository(BaseRepository):
    """
    Handles all database-level operations for User entity.
    Each method includes logging for better observability and error tracking.
    """

    async def get_all(self):
        logger.info("Fetching all non-deleted users.")
        try:
            users = self.db.query(User).filter(User.is_deleted == 0).all()
            logger.success(f"Fetched {len(users)} users successfully.")
            return users
        except SQLAlchemyError as e:
            logger.exception("Database error while fetching all users.")
            raise

    async def get_by_id(self, user_id: int):
        logger.info(f"Fetching user by ID: {user_id}")
        try:
            user = self.db.query(User).filter(
                User.user_id == user_id, User.is_deleted == 0).first()
            if not user:
                logger.warning(f"User with ID {user_id} not found.")
            else:
                logger.success(f"User {user_id} fetched successfully.")
            return user
        except SQLAlchemyError as e:
            logger.exception(f"Database error while fetching user {user_id}.")
            raise

    async def get_by_bio_id(self, bio_id: int):
        logger.info(f"Fetching user by ID: {bio_id}")
        try:
            user = self.db.query(User).filter(
                User.bio_id == bio_id, User.is_deleted == 0).all()
            if not user:
                logger.warning(f"User with ID {bio_id} not found.")
            else:
                logger.success(f"User {bio_id} fetched successfully.")
            return user
        except SQLAlchemyError as e:
            logger.exception(f"Database error while fetching user {bio_id}.")
            raise

    async def create(self, user: User):
        logger.info(f"Creating new user: {user.user_name}")
        try:
            self.add(user)
            self.commit()
            self.refresh(user)
            logger.success(f"User {user.user_id} created successfully.")
            return user
        except SQLAlchemyError as e:
            self.rollback()
            logger.exception(
                f"Database error while creating user '{user.user_name}'.")
            raise

    async def update(self, user: User):
        logger.info(f"Updating user: {user.user_id}")
        try:
            self.commit()
            self.refresh(user)
            logger.success(f"User {user.user_id} updated successfully.")
            return user
        except SQLAlchemyError as e:
            self.rollback()
            logger.exception(
                f"Database error while updating user {user.user_id}.")
            raise
