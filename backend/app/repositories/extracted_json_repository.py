from sqlalchemy.exc import SQLAlchemyError
from app.models.extracted_json_model import ReturnJson
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger
from app.core.result import Result


class ReturnJsonRepository(BaseRepository):
    """
    Handles all database-level operations for ReturnJson entity.
    Logging is limited to exceptions only.
    """

    async def get_all(self) -> Result:
        try:
            records = self.db.query(ReturnJson).filter(ReturnJson.is_deleted == 0).all()
            return Result.Ok(data=records)
        except SQLAlchemyError:
            logger.exception("Database error while fetching return JSON records.")
            return Result.Fail("Database error while fetching return JSON records", code=500)

    async def get_by_id(self, return_id: int) -> Result:
        try:
            record = self.db.query(ReturnJson).filter(
                ReturnJson.return_id == return_id, ReturnJson.is_deleted == 0).first()
            if not record:
                return Result.Fail(f"Return JSON {return_id} not found", code=404)
            return Result.Ok(data=record)
        except SQLAlchemyError:
            logger.exception(f"Database error while fetching return JSON {return_id}.")
            return Result.Fail("Database error while fetching return JSON", code=500)

    async def create(self, record: ReturnJson) -> Result:
        try:
            self.add(record)
            self.commit()
            self.refresh(record)
            return Result.Ok(data=record)
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Error creating return JSON.")
            return Result.Fail("Database error while creating return JSON", code=500)

    async def update(self, record: ReturnJson) -> Result:
        try:
            self.commit()
            self.refresh(record)
            return Result.Ok(data=record)
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Error updating return JSON.")
            return Result.Fail("Database error while updating return JSON", code=500)
