from fastapi import status
from app.schemas.response_schema import CommonResponse

def success_response(data=None, message="Success", code=status.HTTP_200_OK):
    return CommonResponse(
        response_status=True,
        status_code=code,
        message=message,
        source_output=data
    )

def error_response(message="Error", code=status.HTTP_400_BAD_REQUEST):
    return CommonResponse(
        response_status=False,
        status_code=code,
        message=message,
        source_output=None
    )
