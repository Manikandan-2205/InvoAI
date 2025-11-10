from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder


class ApiResponse:
    @staticmethod
    def success(message="Success", code=status.HTTP_200_OK, data=None):
        return JSONResponse(
            status_code=code,
            content=jsonable_encoder({
                "response_status": True,
                "message": message,
                "source_output": data,
            }),
        )

    @staticmethod
    def error(message="Error", code=status.HTTP_400_BAD_REQUEST, details=None):
        return JSONResponse(
            status_code=code,
            content=jsonable_encoder({
                "response_status": False,
                "message": message,
                "source_output": details,
            }),
        )
