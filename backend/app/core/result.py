from fastapi import status
from pydantic import BaseModel
from typing import Any, Optional


class Result(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: str = ""
    code: int = status.HTTP_200_OK

    @classmethod
    def Ok(cls, data=None, message: str = "Success", code: int = status.HTTP_200_OK):
        return cls(success=True, data=data, message=message, code=code)

    @classmethod
    def Fail(cls, message: str = "Error", code: int = status.HTTP_400_BAD_REQUEST):
        return cls(success=False, data=None, message=message, code=code)

    def to_response(self):
        """Convert Result to ApiResponse automatically"""
        from app.utils.api_response import ApiResponse
        if self.success:
            return ApiResponse.success(self.data, self.message, self.code)
        else:
            return ApiResponse.error(self.message, self.code, self.data)
