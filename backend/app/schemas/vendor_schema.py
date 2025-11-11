from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VendorBase(BaseModel):
    vendor_name: str = Field(..., max_length=100)
    is_deleted: Optional[int] = 0

    class Config:
        orm_mode = True

class VendorCreate(VendorBase):
    created_by: Optional[int] = None

class VendorUpdate(BaseModel):
    vendor_name: Optional[str] = None
    is_deleted: Optional[int] = None

    class Config:
        orm_mode = True

class VendorResponse(VendorBase):
    vendor_id: int
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
