from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.services.extracted_json_service import ReturnJsonService
from app.schemas.extracted_json_schema import ReturnJsonCreate, ReturnJsonUpdate
from app.core.database import get_db
from app.utils.api_response import ApiResponse
from app.core.logger import logger
from app.repositories.extracted_json_repository import ReturnJsonRepository


router = APIRouter()


def get_return_json_service(db: Session = Depends(get_db)) -> ReturnJsonService:
    repo = ReturnJsonRepository(db)
    return ReturnJsonService(repo)


@router.get("/", summary="Get all return JSON records")
async def get_all_returns(service: ReturnJsonService = Depends(get_return_json_service)):
    try:
        result = await service.get_all_returns()
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception("Error fetching return JSON records.")
        return ApiResponse.error(str(e), 500)


@router.get("/{return_id}", summary="Get return JSON by ID")
async def get_return_by_id(return_id: int, service: ReturnJsonService = Depends(get_return_json_service)):
    try:
        result = await service.get_return_by_id(return_id)
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception(f"Error fetching return JSON {return_id}")
        return ApiResponse.error(str(e), 500)


@router.post("/", summary="Create return JSON", status_code=status.HTTP_201_CREATED)
async def create_return(payload: ReturnJsonCreate, service: ReturnJsonService = Depends(get_return_json_service)):
    try:
        result = await service.create_return(payload)
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception("Error creating return JSON.")
        return ApiResponse.error(str(e), 500)


@router.put("/{return_id}", summary="Update return JSON")
async def update_return(return_id: int, payload: ReturnJsonUpdate, service: ReturnJsonService = Depends(get_return_json_service)):
    try:
        result = await service.update_return(return_id, payload)
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception(f"Error updating return JSON {return_id}")
        return ApiResponse.error(str(e), 500)


@router.delete("/{return_id}", summary="Soft delete return JSON", status_code=status.HTTP_204_NO_CONTENT)
async def delete_return(return_id: int, service: ReturnJsonService = Depends(get_return_json_service)):
    try:
        result = await service.soft_delete_return(return_id)
        return ApiResponse.from_result(result)
    except Exception as e:
        logger.exception(f"Error deleting return JSON {return_id}")
        return ApiResponse.error(str(e), 500)
