from sqlalchemy.exc import SQLAlchemyError
from app.models.extraction_model import Extraction
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger


class ExtractionRepository(BaseRepository):
    """
    Handles all database-level operations for Extraction entity.
    """

    async def get_all(self):
        logger.info("Fetching all non-deleted extractions.")
        try:
            extractions = self.db.query(Extraction).filter(Extraction.is_deleted == 0).all()
            logger.success(f"Fetched {len(extractions)} extractions successfully.")
            return extractions
        except SQLAlchemyError:
            logger.exception("Database error while fetching extractions.")
            raise

    async def get_by_id(self, extraction_id: int):
        logger.info(f"Fetching extraction by ID: {extraction_id}")
        try:
            extraction = self.db.query(Extraction).filter(
                Extraction.extraction_id == extraction_id, Extraction.is_deleted == 0).first()
            if not extraction:
                logger.warning(f"Extraction {extraction_id} not found.")
            else:
                logger.success(f"Extraction {extraction_id} fetched successfully.")
            return extraction
        except SQLAlchemyError:
            logger.exception(f"Database error while fetching extraction {extraction_id}.")
            raise

    async def create(self, extraction: Extraction):
        logger.info(f"Creating extraction: {extraction.extraction_name}")
        try:
            self.add(extraction)
            self.commit()
            self.refresh(extraction)
            logger.success(f"Extraction {extraction.extraction_id} created.")
            return extraction
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Error creating extraction.")
            raise

    async def update(self, extraction: Extraction):
        logger.info(f"Updating extraction: {extraction.extraction_id}")
        try:
            self.commit()
            self.refresh(extraction)
            logger.success(f"Extraction {extraction.extraction_id} updated.")
            return extraction
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Error updating extraction.")
            raise
