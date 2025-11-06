
from pydantic import BaseModel
from typing import Optional, Any

class CommonResponse(BaseModel):
    response_status: bool
    status_code: int
    message: str
    source_output: Optional[Any] = None
