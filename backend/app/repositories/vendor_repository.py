from sqlalchemy.exc import SQLAlchemyError
from app.models.vendor_model import Vendor
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger
from app.core.result import Result


class VendorRepository(BaseRepository):
    """
    Handles all database-level operations for Vendor entity.
    Logging is limited to exceptions only.
    """

    async def get_all(self) -> Result:
        try:
            vendors = self.db.query(Vendor).filter(Vendor.is_deleted == 0).all()
            return Result.Ok(data=vendors)
        except SQLAlchemyError:
            logger.exception("Database error while fetching all vendors.")
            return Result.Fail("Database error while fetching vendors", code=500)

    async def get_by_id(self, vendor_id: int) -> Result:
        try:
            vendor = self.db.query(Vendor).filter(
                Vendor.vendor_id == vendor_id, Vendor.is_deleted == 0).first()
            if not vendor:
                return Result.Fail(f"Vendor with ID {vendor_id} not found", code=404)
            return Result.Ok(data=vendor)
        except SQLAlchemyError:
            logger.exception(f"Database error while fetching vendor {vendor_id}.")
            return Result.Fail("Database error while fetching vendor", code=500)

    async def create(self, vendor: Vendor) -> Result:
        try:
            self.add(vendor)
            self.commit()
            self.refresh(vendor)
            return Result.Ok(data=vendor)
        except SQLAlchemyError:
            self.rollback()
            logger.exception(f"Database error while creating vendor '{vendor.vendor_name}'.")
            return Result.Fail("Database error while creating vendor", code=500)

    async def update(self, vendor: Vendor) -> Result:
        try:
            self.commit()
            self.refresh(vendor)
            return Result.Ok(data=vendor)
        except SQLAlchemyError:
            self.rollback()
            logger.exception(f"Database error while updating vendor {vendor.vendor_id}.")
            return Result.Fail("Database error while updating vendor", code=500)
