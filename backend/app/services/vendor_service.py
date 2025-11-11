from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.models.vendor_model import Vendor
from app.schemas.vendor_schema import VendorCreate, VendorUpdate, VendorResponse
from app.core.result import Result
from app.core.logger import logger
from app.repositories.vendor_repository import VendorRepository


class VendorService:
    """
    Business logic layer for Vendor operations.
    """

    def __init__(self, repo: VendorRepository):
        self.repo = repo

    async def get_all_vendors(self) -> Result:
        try:
            vendors = await self.repo.get_all()
            vendor_list = [VendorResponse.from_orm(v).dict() for v in vendors]
            return Result.Ok(vendor_list, message="Vendors fetched successfully", code=200)
        except SQLAlchemyError:
            logger.exception("Error fetching vendors.")
            return Result.Fail("Database error while fetching vendors", code=500)

    async def get_vendor_by_id(self, vendor_id: int) -> Result:
        try:
            vendor = await self.repo.get_by_id(vendor_id)
            if not vendor:
                return Result.Fail("Vendor not found", code=404)
            vendor_data = VendorResponse.from_orm(vendor).dict()
            return Result.Ok(vendor_data, message="Vendor fetched successfully", code=200)
        except SQLAlchemyError:
            logger.exception(f"Error fetching vendor {vendor_id}.")
            return Result.Fail("Database error while fetching vendor", code=500)

    async def create_vendor(self, data: VendorCreate) -> Result:
        try:
            vendor = Vendor(
                vendor_name=data.vendor_name,
                created_by=data.created_by,
                created_at=datetime.now(),
                is_deleted=data.is_deleted,
            )
            created = await self.repo.create(vendor)
            vendor_data = VendorResponse.from_orm(created).dict()
            return Result.Ok(vendor_data, message="Vendor created successfully", code=201)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Database error while creating vendor.")
            return Result.Fail("Database error while creating vendor", code=500)
        except Exception as e:
            self.repo.rollback()
            logger.exception("Unexpected error while creating vendor.")
            return Result.Fail(str(e), code=500)

    async def update_vendor(self, vendor_id: int, data: VendorUpdate) -> Result:
        existing = await self.repo.get_by_id(vendor_id)
        if not existing:
            return Result.Fail("Vendor not found", code=404)

        try:
            if data.vendor_name is not None:
                existing.vendor_name = data.vendor_name
            if data.is_deleted is not None:
                existing.is_deleted = data.is_deleted

            updated = await self.repo.update(existing)
            vendor_data = VendorResponse.from_orm(updated).dict()
            return Result.Ok(vendor_data, message="Vendor updated successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error updating vendor.")
            return Result.Fail("Database error while updating vendor", code=500)

    async def soft_delete_vendor(self, vendor_id: int) -> Result:
        existing = await self.repo.get_by_id(vendor_id)
        if not existing:
            return Result.Fail("Vendor not found", code=404)

        try:
            existing.is_deleted = 1
            updated = await self.repo.update(existing)
            vendor_data = VendorResponse.from_orm(updated).dict()
            return Result.Ok(vendor_data, message="Vendor deleted successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Error deleting vendor.")
            return Result.Fail("Database error while deleting vendor", code=500)
