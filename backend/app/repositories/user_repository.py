from sqlalchemy.exc import SQLAlchemyError
from app.models.user_model import User
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger

class UserRepository(BaseRepository):
    """
    Handles all database-level operations for User entity.
    """

    def get_all(self):
        logger.debug("Querying all non-deleted users from DB.")
        try:
            return self.db.query(User).filter(User.is_deleted == 0).all()
        except SQLAlchemyError as e:
            logger.exception("Error fetching all users from DB.")
            raise e

    def get_by_id(self, user_id: int):
        logger.debug(f"Querying user by ID: {user_id}")
        return self.db.query(User).filter(User.user_id == user_id, User.is_deleted == 0).first()

    def create(self, user: User):
        logger.debug(f"Adding new user: {user.user_name}")
        self.add(user)
        self.commit()
        self.refresh(user)
        return user

    def update(self, user: User):
        logger.debug(f"Updating user: {user.user_id}")
        self.commit()
        self.refresh(user)
        return user
