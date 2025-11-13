from pydantic import BaseModel, Field, constr
from typing import Optional, List
from datetime import datetime


# BASE SCHEMA
class UserBase(BaseModel):
    bio_id: Optional[int] = Field(None, description="Linked Bio ID")
    user_name: Optional[str] = Field(
        None, strip_whitespace=True, min_length=3, max_length=25)

    class Config:
        from_attributes = True  # For Pydantic v2 ORM support


# CREATE / UPDATE SCHEMAS
class UserCreate(UserBase):
    password: constr(min_length=1, max_length=250)
    created_by: Optional[int] = None


class UserUpdate(UserBase):
    updated_by: Optional[int] = None


class PasswordUpdate(BaseModel):
    password: constr(min_length=1, max_length=250)
    updated_by: Optional[int] = None


# RESPONSE SCHEMAS
class UserResponse(UserBase):
    user_id: int
    created_by: Optional[int]
    created_at: Optional[datetime]
    updated_by: Optional[int]
    updated_at: Optional[datetime]


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int


# GENERIC RESPONSE WRAPPER
class GenericResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    code: Optional[int] = 200
