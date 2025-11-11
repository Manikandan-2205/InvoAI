from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.log_model import Log
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger
from typing import Optional
from datetime import datetime


class AuthRepository(BaseRepository):
    """
    Handles authentication and login logging.
    """

    async def verify_user(self, user_name: str) -> Optional[User]:
        logger.info(f"Verifying user: {user_name}")
        try:
            user = self.db.query(User).filter(
                User.user_name == user_name, User.is_deleted == 0).first()
            return user
        except SQLAlchemyError:
            logger.exception("Database error during user verification.")
            raise

    async def save_login_log(self, user_id: int, login_time: datetime) -> Log:
        logger.info(f"Saving login log for user_id: {user_id}")
        try:
            log = Log(user_id=user_id, login_time=login_time)
            self.add(log)
            self.commit()
            self.refresh(log)
            logger.success(f"Login log {log.log_id} saved.")
            return log
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Database error while saving login log.")
            raise
