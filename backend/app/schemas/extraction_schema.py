from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExtractionBase(BaseModel):
    extraction_name: str = Field(..., max_length=50)
    x_min: Optional[int] = None
    x_max: Optional[int] = None
    y_min: Optional[int] = None
    y_max: Optional[int] = None
    vendor_id: Optional[int] = None
    is_deleted: Optional[int] = 0

    class Config:
        orm_mode = True

class ExtractionCreate(ExtractionBase):
    created_by: Optional[int] = None

class ExtractionUpdate(BaseModel):
    extraction_name: Optional[str] = None
    x_min: Optional[int] = None
    x_max: Optional[int] = None
    y_min: Optional[int] = None
    y_max: Optional[int] = None
    vendor_id: Optional[int] = None
    is_deleted: Optional[int] = None
    updated_by: Optional[int] = None

    class Config:
        orm_mode = True

class ExtractionResponse(ExtractionBase):
    extraction_id: int
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    updated_at: Optional[datetime] = None
