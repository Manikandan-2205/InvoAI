import structlog
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class RequestContextLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=str(request.url.path),
            method=request.method,
        )
        response = await call_next(request)
        structlog.contextvars.clear_contextvars()
        return response
