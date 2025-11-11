from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ReturnJsonBase(BaseModel):
    invoice_number: Optional[str] = Field(None, max_length=30)
    extracted_json: Optional[Dict[str, Any]] = None
    vendor_id: Optional[int] = None
    is_deleted: Optional[int] = 0

    class Config:
        orm_mode = True

class ReturnJsonCreate(ReturnJsonBase):
    created_by: Optional[int] = None

class ReturnJsonUpdate(BaseModel):
    invoice_number: Optional[str] = None
    extracted_json: Optional[Dict[str, Any]] = None
    vendor_id: Optional[int] = None
    is_deleted: Optional[int] = None

    class Config:
        orm_mode = True

class ReturnJsonResponse(ReturnJsonBase):
    return_id: int
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
