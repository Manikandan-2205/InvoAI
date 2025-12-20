from sqlalchemy.exc import SQLAlchemyError
from app.core.result import Result
from app.repositories.global_repository import GlobalRepository
from app.schemas.global_schema import GlobalVendorList
from app.core.logger import logger

class GobalService:
    def __init__(self, gobalrepo: GlobalRepository):
        self.gobalrepo = gobalrepo
        
    async def vendor_list(self) -> Result:
        try:
            vendors = await self.gobalrepo.get_all_vendor()

            if not vendors.success or not vendors.data:
                return Result.Fail("No active vendors found", code=404)

            vendor_list = [
                GlobalVendorList.from_orm(v).dict(by_alias=False)
                for v in vendors.data
            ]

            print(" Vendor List: ", vendor_list)
            return Result.Ok(
                data=vendor_list,
                message="Active vendors fetched successfully",
                code=200
            )

        except SQLAlchemyError as e:
            logger.exception("Database error while fetching active vendors.")
            return Result.Fail(str(e), code=500)

        except Exception as e:
            logger.exception(str(e))
            return Result.Fail(str(e), code=500)
