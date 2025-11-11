from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    user_name: str = Field(..., max_length=25)
    password: str = Field(...)

class LoginResponse(BaseModel):
    bio_id: int
    user_name: str
    login_time: datetime
