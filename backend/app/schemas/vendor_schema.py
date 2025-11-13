from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class VendorBase(BaseModel):
    vendor_name: str = Field(..., max_length=100)
    is_deleted: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

class VendorCreate(VendorBase):
    created_by: Optional[int] = None

class VendorUpdate(BaseModel):     
    vendor_name: str = Field(..., max_length=100)
    is_deleted: Optional[int] = 0
    updated_by : int  

class VendorResponse(VendorBase):
    vendor_id: int
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None

