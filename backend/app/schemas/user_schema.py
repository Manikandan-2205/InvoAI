from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base shared schema
class UserBase(BaseModel):
    user_name: str = Field(..., max_length=25)
    bio_id: Optional[int] = None
    is_deleted: Optional[int] = 0

# Create schema (for POST requests)
class UserCreate(UserBase):
    password_hash: str = Field(..., max_length=250)
    created_by: Optional[int] = None

# Update schema
class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    password_hash: Optional[str] = None
    updated_by: Optional[int] = None
    is_deleted: Optional[int] = 0

# Response schema
class UserResponse(UserBase):
    user_id: int
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
