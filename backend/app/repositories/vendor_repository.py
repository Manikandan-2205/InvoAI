from sqlalchemy.exc import SQLAlchemyError
from app.models.vendor_model import Vendor
from app.repositories.base_repository import BaseRepository
from app.core.logger import logger


class VendorRepository(BaseRepository):
    """
    Handles all database-level operations for Vendor entity.
    Each method includes logging for better observability and error tracking.
    """

    async def get_all(self):
        logger.info("Fetching all non-deleted vendors.")
        try:
            vendors = self.db.query(Vendor).filter(Vendor.is_deleted == 0).all()
            logger.success(f"Fetched {len(vendors)} vendors successfully.")
            return vendors
        except SQLAlchemyError:
            logger.exception("Database error while fetching all vendors.")
            raise

    async def get_by_id(self, vendor_id: int):
        logger.info(f"Fetching vendor by ID: {vendor_id}")
        try:
            vendor = self.db.query(Vendor).filter(
                Vendor.vendor_id == vendor_id, Vendor.is_deleted == 0).first()
            if not vendor:
                logger.warning(f"Vendor with ID {vendor_id} not found.")
            else:
                logger.success(f"Vendor {vendor_id} fetched successfully.")
            return vendor
        except SQLAlchemyError:
            logger.exception(f"Database error while fetching vendor {vendor_id}.")
            raise

    async def create(self, vendor: Vendor):
        logger.info(f"Creating new vendor: {vendor.vendor_name}")
        try:
            self.add(vendor)
            self.commit()
            self.refresh(vendor)
            logger.success(f"Vendor {vendor.vendor_id} created successfully.")
            return vendor
        except SQLAlchemyError:
            self.rollback()
            logger.exception(f"Database error while creating vendor '{vendor.vendor_name}'.")
            raise

    async def update(self, vendor: Vendor):
        logger.info(f"Updating vendor: {vendor.vendor_id}")
        try:
            self.commit()
            self.refresh(vendor)
            logger.success(f"Vendor {vendor.vendor_id} updated successfully.")
            return vendor
        except SQLAlchemyError:
            self.rollback()
            logger.exception(f"Database error while updating vendor {vendor.vendor_id}.")
            raise
