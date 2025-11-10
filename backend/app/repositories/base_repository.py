from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import logger


class BaseRepository:
    """
    Base repository that wraps SQLAlchemy Session with safe commit/rollback operations.
    Provides consistent logging and exception handling for derived repositories.
    """

    def __init__(self, db: Session):
        self.db = db

    def add(self, entity):
        try:
            self.db.add(entity)
            logger.debug(f"Entity added to session: {entity}")
            return entity
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.exception(f"Error adding entity: {e}")
            raise

    def commit(self):
        try:
            self.db.commit()
            logger.debug("Transaction committed successfully.")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.exception(f"Error committing transaction: {e}")
            raise

    def rollback(self):
        try:
            self.db.rollback()
            logger.warning("Transaction rolled back.")
        except Exception as e:
            logger.exception(f"Error during rollback: {e}")
            raise

    def refresh(self, entity):
        try:
            self.db.refresh(entity)
            logger.debug(f"Entity refreshed from database: {entity}")
            return entity
        except SQLAlchemyError as e:
            logger.exception(f"Error refreshing entity: {e}")
            raise
