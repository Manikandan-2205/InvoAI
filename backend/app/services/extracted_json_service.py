from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.models.extracted_json_model import ReturnJson
from app.schemas.extracted_json_schema import ReturnJsonCreate, ReturnJsonUpdate, ReturnJsonResponse
from app.core.result import Result
from app.core.logger import logger
from app.repositories.extracted_json_repository import ReturnJsonRepository


class OCRExtractionService:
    """
    Business logic layer for ReturnJson operations.
    """

    def __init__(self, repo: ReturnJsonRepository):
        self.repo = repo

    async def get_all_returns(self) -> Result:
        try:
            records = await self.repo.get_all()
            data = [ReturnJsonResponse.from_orm(r).dict() for r in records]
            return Result.Ok(data, message="Return JSON records fetched successfully", code=200)
        except SQLAlchemyError:
            logger.exception("Error fetching return JSON records.")
            return Result.Fail("Database error while fetching return JSON records", code=500)

    async def get_return_by_id(self, return_id: int) -> Result:
        try:
            record = await self.repo.get_by_id(return_id)
            if not record:
                return Result.Fail("Return JSON not found", code=404)
            data = ReturnJsonResponse.from_orm(record).dict()
            return Result.Ok(data, message="Return JSON fetched successfully", code=200)
        except SQLAlchemyError:
            logger.exception(f"Error fetching return JSON {return_id}.")
            return Result.Fail("Database error while fetching return JSON", code=500)

    async def create_return(self, data: ReturnJsonCreate) -> Result:
        try:
            record = ReturnJson(
                invoice_number=data.invoice_number,
                extracted_json=data.extracted_json,
                vendor_id=data.vendor_id,
                created_by=data.created_by,
                created_at=datetime.now(),
                is_deleted=data.is_deleted,
            )
            created = await self.repo.create(record)
            data = ReturnJsonResponse.from_orm(created).dict()
            return Result.Ok(data, message="Return JSON created successfully", code=201)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error creating return JSON.")
            return Result.Fail("Database error while creating return JSON", code=500)

    async def update_return(self, return_id: int, data: ReturnJsonUpdate) -> Result:
        existing = await self.repo.get_by_id(return_id)
        if not existing:
            return Result.Fail("Return JSON not found", code=404)

        try:
            for field, value in data.dict(exclude_unset=True).items():
                setattr(existing, field, value)
            updated = await self.repo.update(existing)
            data = ReturnJsonResponse.from_orm(updated).dict()
            return Result.Ok(data, message="Return JSON updated successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error updating return JSON.")
            return Result.Fail("Database error while updating return JSON", code=500)

    async def soft_delete_return(self, return_id: int) -> Result:
        existing = await self.repo.get_by_id(return_id)
        if not existing:
            return Result.Fail("Return JSON not found", code=404)

        try:
            existing.is_deleted = 1
            updated = await self.repo.update(existing)
            data = ReturnJsonResponse.from_orm(updated).dict()
            return Result.Ok(data, message="Return JSON deleted successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error deleting return JSON.")
            return Result.Fail("Database error while deleting return JSON", code=500)
