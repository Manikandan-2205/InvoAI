from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.models.extraction_model import Extraction
from app.schemas.extraction_schema import ExtractionCreate, ExtractionUpdate, ExtractionResponse
from app.core.result import Result
from app.core.logger import logger
from app.repositories.extraction_details_repository import ExtractionRepository


class ExtractionService:
    """
    Business logic layer for Extraction operations.
    """

    def __init__(self, repo: ExtractionRepository):
        self.repo = repo

    async def get_all_extractions(self) -> Result:
        try:
            extractions = await self.repo.get_all()
            data = [ExtractionResponse.from_orm(e).dict() for e in extractions]
            return Result.Ok(data, message="Extractions fetched successfully", code=200)
        except SQLAlchemyError:
            logger.exception("Error fetching extractions.")
            return Result.Fail("Database error while fetching extractions", code=500)

    async def get_extraction_by_id(self, extraction_id: int) -> Result:
        try:
            extraction = await self.repo.get_by_id(extraction_id)
            if not extraction:
                return Result.Fail("Extraction not found", code=404)
            data = ExtractionResponse.from_orm(extraction).dict()
            return Result.Ok(data, message="Extraction fetched successfully", code=200)
        except SQLAlchemyError:
            logger.exception(f"Error fetching extraction {extraction_id}.")
            return Result.Fail("Database error while fetching extraction", code=500)

    async def create_extraction(self, data: ExtractionCreate) -> Result:
        try:
            extraction = Extraction(
                extraction_name=data.extraction_name,
                x_min=data.x_min,
                x_max=data.x_max,
                y_min=data.y_min,
                y_max=data.y_max,
                vendor_id=data.vendor_id,
                created_by=data.created_by,
                created_at=datetime.now(),
                is_deleted=data.is_deleted,
            )
            created = await self.repo.create(extraction)
            data = ExtractionResponse.from_orm(created).dict()
            return Result.Ok(data, message="Extraction created successfully", code=201)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error creating extraction.")
            return Result.Fail("Database error while creating extraction", code=500)

    async def update_extraction(self, extraction_id: int, data: ExtractionUpdate) -> Result:
        existing = await self.repo.get_by_id(extraction_id)
        if not existing:
            return Result.Fail("Extraction not found", code=404)

        try:
            for field, value in data.dict(exclude_unset=True).items():
                setattr(existing, field, value)
            existing.updated_at = datetime.now()

            updated = await self.repo.update(existing)
            data = ExtractionResponse.from_orm(updated).dict()
            return Result.Ok(data, message="Extraction updated successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error updating extraction.")
            return Result.Fail("Database error while updating extraction", code=500)

    async def soft_delete_extraction(self, extraction_id: int) -> Result:
        existing = await self.repo.get_by_id(extraction_id)
        if not existing:
            return Result.Fail("Extraction not found", code=404)

        try:
            existing.is_deleted = 1
            existing.updated_at = datetime.now()

            deleted = await self.repo.update(existing)
            data = ExtractionResponse.from_orm(deleted).dict()
            return Result.Ok(data, message="Extraction deleted successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error deleting extraction.")
            return Result.Fail("Database error while deleting extraction", code=500)
