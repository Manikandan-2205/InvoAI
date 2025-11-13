from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.log_model import Log
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger
from app.core.result import Result
from typing import Optional
from datetime import datetime


class AuthRepository(BaseRepository):
    """
    Handles authentication and login logging.
    Logging is limited to exceptions only.
    """

    async def verify_user(self, user_name: str) -> Result:
        try:
            user = self.db.query(User).filter(
                User.user_name == user_name, User.is_deleted == 0).first()
            if not user:
                return Result.Fail(f"User '{user_name}' not found", code=404)
            return Result.Ok(data=user)
        except SQLAlchemyError:
            logger.exception("Database error during user verification.")
            return Result.Fail("Database error during user verification", code=500)

    async def save_login_log(self, user_id: int, login_time: datetime) -> Result:
        try:
            log = Log(user_id=user_id, login_time=login_time)
            self.add(log)
            self.commit()
            self.refresh(log)
            return Result.Ok(data=log)
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Database error while saving login log.")
            return Result.Fail("Database error while saving login log", code=500)

    async def get_users_by_username(self, user_name: str) -> Result:
        try:
            users = await self.session.execute(
                select(User).where(User.user_name ==
                                   user_name, User.is_deleted == 0)
            )
            return Result.Ok(users.scalars().all())
        except SQLAlchemyError as e:
            logger.exception("Error fetching users by username.")
            return Result.Fail("Database error", code=500)
