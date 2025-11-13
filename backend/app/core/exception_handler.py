# app/core/exception_handler.py

from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.utils.api_response import ApiResponse
from app.core.logger import logger
import time

# ============================
# Middleware: Request Logging
# ============================

async def log_requests_middleware(request: Request, call_next):
    """Middleware to log all incoming requests and responses."""
    start_time = time.time()
    try:
        logger.info(f"➡️  {request.method} {request.url.path}")
        response = await call_next(request)
    except Exception as exc:
        logger.exception(f"🔥 Unhandled exception in {request.url.path}: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse.error("Internal server error", code=500).dict(),
        )

    process_time = (time.time() - start_time) * 1000
    logger.info(f"⬅️  {request.method} {request.url.path} - {response.status_code} ({process_time:.2f}ms)")
    return response


# ===========================================
# Global Exception Handler (Catch-All Errors)
# ===========================================

async def global_exception_handler(request: Request, exc: Exception):
    """Catches all unhandled exceptions globally and logs them."""
    logger.exception(f"🌋 Global exception caught for {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response("Unexpected server error", code=500).dict(),
    )


# ===========================================
# Optional: Specific Exception Handlers
# ===========================================
# You can expand this for known exceptions, for example:
#
# from fastapi.exceptions import RequestValidationError
# from starlette.exceptions import HTTPException as StarletteHTTPException
#
# async def http_exception_handler(request: Request, exc: StarletteHTTPException):
#     logger.warning(f"⚠️ HTTP Exception: {exc.detail}")
#     return JSONResponse(
#         status_code=exc.status_code,
#         content=error_response(exc.detail, code=exc.status_code).dict(),
#     )
#
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     logger.warning(f"❌ Validation error: {exc.errors()}")
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=error_response("Validation failed", code=422).dict(),
#     )
