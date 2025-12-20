from fastapi import APIRouter, Depends
from app.core.database import get_db
from sqlalchemy.orm import Session

from app.services.global_service import GobalService
from app.utils.api_response import ApiResponse
from app.core.logger import logger
from app.repositories.global_repository import GlobalRepository

router = APIRouter()

def get_vendor_service(db: Session = Depends(get_db)) -> GobalService:
    """Dependency to inject VendorService."""
    repo = GlobalRepository(db)
    return GobalService(repo)

@router.get("/get-all-list", summary="Get all vendors")
async def get_all_vendors(service: GobalService = Depends(get_vendor_service)):
    try:
        result = await service.vendor_list()
        if not result.success:
            return ApiResponse.error(result.message, result.code)
        return ApiResponse.success(result.message, result.code, result.data)
    except Exception as e:
        logger.exception("Error fetching vendors.")
        return ApiResponse.error(str(e), 500)