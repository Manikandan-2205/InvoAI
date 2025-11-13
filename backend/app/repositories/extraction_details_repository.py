from sqlalchemy.exc import SQLAlchemyError
from app.models.extraction_model import Extraction
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger
from app.core.result import Result


class ExtractionRepository(BaseRepository):
    """
    Handles all database-level operations for Extraction entity.
    Logging is limited to exceptions only.
    """

    async def get_all(self) -> Result:
        try:
            extractions = self.db.query(Extraction).filter(Extraction.is_deleted == 0).all()
            return Result.Ok(data=extractions)
        except SQLAlchemyError:
            logger.exception("Database error while fetching extractions.")
            return Result.Fail("Database error while fetching extractions", code=500)

    async def get_by_id(self, extraction_id: int) -> Result:
        try:
            extraction = self.db.query(Extraction).filter(
                Extraction.extraction_id == extraction_id, Extraction.is_deleted == 0).first()
            if not extraction:
                return Result.Fail(f"Extraction {extraction_id} not found", code=404)
            return Result.Ok(data=extraction)
        except SQLAlchemyError:
            logger.exception(f"Database error while fetching extraction {extraction_id}.")
            return Result.Fail("Database error while fetching extraction", code=500)

    async def create(self, extraction: Extraction) -> Result:
        try:
            self.add(extraction)
            self.commit()
            self.refresh(extraction)
            return Result.Ok(data=extraction)
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Error creating extraction.")
            return Result.Fail("Database error while creating extraction", code=500)

    async def update(self, extraction: Extraction) -> Result:
        try:
            self.commit()
            self.refresh(extraction)
            return Result.Ok(data=extraction)
        except SQLAlchemyError:
            self.rollback()
            logger.exception("Error updating extraction.")
            return Result.Fail("Database error while updating extraction", code=500)
