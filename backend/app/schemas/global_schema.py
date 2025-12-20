from pydantic import BaseModel, Field
from typing import Optional

class GlobalVendorList(BaseModel):
    id: Optional[int] = Field(None, alias="vendor_id")
    vendor_name: str = Field(..., max_length=100)

    class Config:
        from_attributes = True
        populate_by_name = True
