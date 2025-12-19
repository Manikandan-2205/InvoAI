from sqlalchemy import desc
from backend.app.models.vendor_model import Vendor
from app.repositories.base_repository import BaseRepository
from app.core.result import Result
from app.core.logger import logger
from sqlalchemy.exc import SQLAlchemyError


class GlobalRepository(BaseRepository):

    async def get_all_vendor(self) -> Result:
        try:
            vendors = self.db.query(Vendor).order_by(desc(Vendor.id)).all()
            return Result.Ok(data=vendors)
        except SQLAlchemyError as ex:
            logger.exception(str(ex))
            return Result.Fail("Database error while fetching vendors", code=500)
