from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.services.extraction_details_service import ExtractionService
from app.schemas.extraction_schema import ExtractionCreate, ExtractionUpdate
from app.core.database import get_db
from app.utils.api_response import ApiResponse
from app.core.logger import logger
from app.repositories.extraction_details_repository import ExtractionRepository

router = APIRouter()

def get_extraction_service(db: Session = Depends(get_db)) -> ExtractionService:
    repo = ExtractionRepository(db)
    return ExtractionService(repo)

@router.get("/", summary="Get all extractions")
async def get_all_extractions(service: ExtractionService = Depends(get_extraction_service)):
    try:
        result = await service.get_all_extractions()
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception("Error fetching extractions.")
        return ApiResponse.error(str(e), 500)

@router.get("/{extraction_id}", summary="Get extraction by ID")
async def get_extraction_by_id(extraction_id: int, service: ExtractionService = Depends(get_extraction_service)):
    try:
        result = await service.get_extraction_by_id(extraction_id)
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception(f"Error fetching extraction {extraction_id}")
        return ApiResponse.error(str(e), 500)

@router.post("/", summary="Create new extraction", status_code=status.HTTP_201_CREATED)
async def create_extraction(payload: ExtractionCreate, service: ExtractionService = Depends(get_extraction_service)):
    try:
        result = await service.create_extraction(payload)
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception("Error creating extraction.")
        return ApiResponse.error(str(e), 500)

@router.put("/{extraction_id}", summary="Update extraction")
async def update_extraction(extraction_id: int, payload: ExtractionUpdate, service: ExtractionService = Depends(get_extraction_service)):
    try:
        result = await service.update_extraction(extraction_id, payload)
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception(f"Error updating extraction {extraction_id}")
        return ApiResponse.error(str(e), 500)

@router.delete("/{extraction_id}", summary="Soft delete extraction", status_code=status.HTTP_204_NO_CONTENT)
async def delete_extraction(extraction_id: int, service: ExtractionService = Depends(get_extraction_service)):
    try:
        result = await service.soft_delete_extraction(extraction_id)
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception(f"Error deleting extraction {extraction_id}")
        return ApiResponse.error(str(e), 500)
