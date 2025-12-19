from pydantic import BaseModel,Field
from typing import Optional,List

class BaseEntry(BaseModel):
    id : Optional[int] = Field(None, description= "Id was required.")
    class Config:
        from_attributes = True


class vendorMaster(BaseEntry):
    vendor_name: str = Field(..., max_length=100)