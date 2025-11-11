from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.services.vendor_service import VendorService
from app.schemas.vendor_schema import VendorCreate, VendorUpdate
from app.core.database import get_db
from app.utils.api_response import ApiResponse
from app.core.logger import logger
from app.repositories.vendor_repository import VendorRepository

router = APIRouter()


def get_vendor_service(db: Session = Depends(get_db)) -> VendorService:
    """Dependency to inject VendorService."""
    repo = VendorRepository(db)
    return VendorService(repo)


@router.get("/", summary="Get all vendors")
async def get_all_vendors(service: VendorService = Depends(get_vendor_service)):
    try:
        result = await service.get_all_vendors()
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception("Error fetching vendors.")
        return ApiResponse.error(str(e), 500)


@router.get("/{vendor_id}", summary="Get vendor by ID")
async def get_vendor_by_id(vendor_id: int, service: VendorService = Depends(get_vendor_service)):
    try:
        result = await service.get_vendor_by_id(vendor_id)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception(f"Error fetching vendor {vendor_id}")
        return ApiResponse.error(str(e), 500)


@router.post("/", summary="Create new vendor", status_code=status.HTTP_201_CREATED)
async def create_vendor(payload: VendorCreate, service: VendorService = Depends(get_vendor_service)):
    try:
        result = await service.create_vendor(payload)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception("Error creating vendor.")
        return ApiResponse.error(str(e), 500)


@router.put("/{vendor_id}", summary="Update existing vendor")
async def update_vendor(vendor_id: int, payload: VendorUpdate, service: VendorService = Depends(get_vendor_service)):
    try:
        result = await service.update_vendor(vendor_id, payload)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception(f"Error updating vendor {vendor_id}")
        return ApiResponse.error(str(e), 500)


@router.delete("/{vendor_id}", summary="Soft delete vendor", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor(vendor_id: int, service: VendorService = Depends(get_vendor_service)):
    try:
        result = await service.soft_delete_vendor(vendor_id)
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception(f"Error deleting vendor {vendor_id}")
        return ApiResponse.error(str(e), 500)
