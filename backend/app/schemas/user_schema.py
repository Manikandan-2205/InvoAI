from pydantic import BaseModel, Field, constr
from typing import Optional
from datetime import datetime



# BASE SCHEMA
class UserBase(BaseModel):
    """
    Shared base schema containing fields common to multiple actions.
    """
    bio_id: Optional[int] = Field(None, description="Linked Bio ID")
    user_name: constr(strip_whitespace=True, min_length=3, max_length=25) = Field(
        ..., description="Unique username"
    )
    
    class Config:
        orm_mode = True

# CREATE / UPDATE SCHEMAS
class UserCreate(UserBase):
    """
    Schema used when creating a new user.
    """
    password: constr(min_length=1, max_length=250) = Field(...,
                                                           description="User password")
    created_by: Optional[int] = Field(None, description="ID of the creator")


class UserUpdate(UserBase):
    """
    Schema used when updating an existing user.
    """
    updated_by: Optional[int] = Field(
        None, description="ID of the person updating this record")


class PasswordUpdate(BaseModel):
    """
    Schema used when updating only a user's password.
    """
    password: constr(min_length=6, max_length=250) = Field(...,
                                                           description="New password")
    updated_by: Optional[int] = Field(
        None, description="ID of the user performing the password update")


# RESPONSE SCHEMAS
class UserResponse(UserBase):
    """
    Schema returned when reading a single user from the API.
    Mirrors the SQLAlchemy model.
    """
    user_id: int = Field(..., description="Unique identifier for the user")
    created_by: Optional[int] = Field(None, description="ID of the creator")
    created_at: Optional[datetime] = Field(
        None, description="Timestamp when user was created")
    updated_by: Optional[int] = Field(
        None, description="ID of the last updater")
    updated_at: Optional[datetime] = Field(
        None, description="Timestamp of last update")
    is_deleted: int = Field(
        0, description="Soft delete flag (0 = active, 1 = deleted)")

    class Config:
        from_attributes = True  # ✅ Works for ORM mapping (Pydantic v2)
        # orm_mode = True  # Uncomment this if using Pydantic v1


class UserListResponse(BaseModel):
    """
    Schema for returning multiple users along with a total count.
    """
    users: list[UserResponse] = Field(..., description="List of user records")
    total: int = Field(..., description="Total number of active users")


# GENERIC RESPONSE WRAPPER (OPTIONAL)
class GenericResponse(BaseModel):
    """
    Common response format for all API endpoints.
    """
    success: bool = Field(..., description="True if the request succeeded")
    message: str = Field(..., description="Descriptive message")
    data: Optional[dict] = Field(None, description="Returned payload, if any")
    code: Optional[int] = Field(200, description="HTTP-like response code")
