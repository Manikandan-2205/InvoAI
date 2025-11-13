from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.core.database import Base, engine
from app.core.config import settings
from app.core.logger import logger
from app.core.exception_handler import log_requests_middleware, global_exception_handler
from app.core.middleware.log_context import RequestContextLogMiddleware

from app.api.v1 import (user_routes_v1, vendor_routes_v1,
                        auth_route_v1,
                        extraction_details_route_v1)
from app.api.v1 import extracted_json_route_v1


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="InvoAI User Management API with Layered Architecture and Auto Documentation",
    contact={"name": "InvoAI Support", "email": "support@invoai.com"},
    license_info={"name": "MIT License"},
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.middleware("http")(log_requests_middleware)
app.add_exception_handler(Exception, global_exception_handler)


app.add_middleware(RequestContextLogMiddleware)


Base.metadata.create_all(bind=engine)
logger.info("✅ Database tables created and engine initialized.")

# Route mappings
app.include_router(auth_route_v1.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(user_routes_v1.router, prefix="/api/v1/user", tags=["User"])
app.include_router(vendor_routes_v1.router,
                   prefix="/api/v1/vendor", tags=["Vendor"])
# app.include_router(extraction_details_route_v1.router,
#                    prefix="/api/v1/extraction-details", tags=["Extraction Details"])
# app.include_router(extracted_json_route_v1.router,
#                    prefix="/api/v1/extracted-json", tags=["Extracted Response"])


# @app.get("/", tags=["Health"], summary="Health Check")
# def root():
#     logger.info("Health check accessed.")
#     return {"message": "InvoAI User Management API is running 🚀"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_redirect():
    return RedirectResponse(url="/docs")

# logger.info("✅ InvoAI API started successfully.")
