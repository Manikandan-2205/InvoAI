from sqlalchemy.exc import SQLAlchemyError
from app.models.extracted_json_model import ReturnJson
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger


class ReturnJsonRepository(BaseRepository):
    """
    Handles all database-level operations for ReturnJson entity.
    """

    async def get_all(self):
        logger.info("Fetching all non-deleted return JSON records.")
        try:
            records = self.db.query(ReturnJson).filter(ReturnJson.is_deleted == 0).all()
            logger.success(f"Fetched {len(records)} records successfully.")
            return records
        except SQLAlchemyError:
            logger.exception("Database error while fetching return JSON records.")
            raise

    async def get_by_id(self, return_id: int):
        logger.info(f"Fetching return JSON by ID: {return_id}")
        try:
            record = self.db.query(ReturnJson).filter(
                ReturnJson.return_id == return_id, ReturnJson.is_deleted == 0).first()
            if not record:
                logger.warning(f"Return JSON {return_id} not found.")
            else:
                logger.success(f"Return JSON {return_id} fetched successfully.")
            return record
        except SQLAlchemyError:
            logger.exception(f"Database error while fetching return JSON {return_id}.")
            raise

    async def create(self, record: ReturnJson):
        logger.info(f"Creating return JSON for invoice: {record.invoice_number}")
        try:
            self.add(record)
            self.commit()
            self.refresh(record)
            logger.success(f"Return JSON {record.return_id} created.")
            return record
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Error creating return JSON.")
            raise

    async def update(self, record: ReturnJson):
        logger.info(f"Updating return JSON: {record.return_id}")
        try:
            self.commit()
            self.refresh(record)
            logger.success(f"Return JSON {record.return_id} updated.")
            return record
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Error updating return JSON.")
            raise
