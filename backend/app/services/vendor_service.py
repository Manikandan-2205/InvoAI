from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.models.vendor_model import Vendor
from app.schemas.vendor_schema import VendorCreate, VendorUpdate, VendorResponse
from app.core.result import Result
from app.core.logger import logger
from app.repositories.vendor_repository import VendorRepository


class VendorService:
    def __init__(self, repo: VendorRepository):
        self.repo = repo

    async def get_all_vendors(self) -> Result:
        try:
            vendors = await self.repo.get_all()

            if not vendors.success or not vendors.data:
                return Result.Fail("No vendors found", code=404)
            
            vendor_list = [VendorResponse.from_orm(v).dict() for v in vendors.data]
            return Result.Ok(vendor_list, message="Vendors fetched successfully", code=200)
        except SQLAlchemyError:
            logger.exception("Database error while fetching vendors.")
            return Result.Fail("Database error while fetching vendors", code=500)
        except Exception as e:
            logger.exception(str(e))
            return Result.Fail(str(e), code=500)

    async def get_vendor_by_id(self, vendor_id: int) -> Result:
        res = await self.repo.get_by_id(vendor_id)
        if not res.success:
            return Result.Fail("Vendor not found", code=404)

        try:
            vendor_data = VendorResponse.from_orm(res.data).dict()
            return Result.Ok(vendor_data, message="Vendor fetched successfully", code=200)
        except SQLAlchemyError:
            logger.exception("Database error while fetching vendor.")
            return Result.Fail("Database error while fetching vendor", code=500)
        except Exception as e:
            logger.exception(str(e))
            return Result.Fail(str(e), code=500)

    async def create_vendor(self, data: VendorCreate) -> Result:
        try:
            vendor = Vendor(
                vendor_name=data.vendor_name,
                created_by=data.created_by,
                created_at=datetime.now(),
                is_deleted=data.is_deleted,
            )
            created = await self.repo.create(vendor)

            if not created.success or not created.data:
                return Result.Fail("Failed to create vendor", code=500)

            vendor_data = VendorResponse.from_orm(created.data).dict()
            return Result.Ok(vendor_data, message="Vendor created successfully", code=201)

        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Database error while creating vendor.")
            return Result.Fail("Database error while creating vendor", code=500)
        except Exception as e:
            self.repo.rollback()
            logger.exception(str(e))
            return Result.Fail(str(e), code=500)


    async def update_vendor(self, vendor_id: int, data: VendorUpdate) -> Result:
        res = await self.repo.get_by_id(vendor_id)
        if not res.success:
            return Result.Fail("Vendor not found", code=404)

        try:
            existing = res.data
            existing.vendor_name = data.vendor_name
            existing.is_deleted = data.is_deleted
            existing.updated_by = data.updated_by
            existing.updated_at = datetime.now()

            updated = await self.repo.update(existing)
            vendor_data = VendorResponse.from_orm(updated.data).dict()
            return Result.Ok(vendor_data, message="Vendor updated successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Database error while updating vendor.")
            return Result.Fail("Database error while updating vendor", code=500)
        except Exception as e:
            self.repo.rollback()
            logger.exception(str(e))
            return Result.Fail(str(e), code=500)

    async def soft_delete_vendor(self, vendor_id: int) -> Result:
        res = await self.repo.get_by_id(vendor_id)
        if not res.success:
            return Result.Fail("Vendor not found", code=404)

        try:
            existing = res.data
            existing.is_deleted = 1            
            existing.updated_at = datetime.now()

            deleted = await self.repo.update(existing)
            if not deleted.success:
                return Result.Fail("Failed to delete vendor", code=500)

            return Result.Ok(message="Vendor deleted successfully", code=200)
        except SQLAlchemyError:
            self.repo.rollback()
            logger.exception("Database error while deleting vendor.")
            return Result.Fail("Database error while deleting vendor", code=500)
        except Exception as e:
            self.repo.rollback()
            logger.exception(str(e))
            return Result.Fail(str(e), code=500)
