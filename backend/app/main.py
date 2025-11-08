from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.core.config import settings
from app.core.logger import logger
from app.core.exception_handler import log_requests_middleware, global_exception_handler

# Import versioned routes
from app.api.v1 import user_routes_v1 as user_routes_v1

from fastapi.responses import RedirectResponse

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="InvoAI User Management API with Layered Architecture and Auto Documentation",
    contact={"name": "InvoAI Support", "email": "support@invoai.com"},
    license_info={"name": "MIT License"},
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middleware + Global Exception
app.middleware("http")(log_requests_middleware)
app.add_exception_handler(Exception, global_exception_handler)

# Initialize DB
Base.metadata.create_all(bind=engine)
logger.info("✅ Database tables created and engine initialized.")

# Routers
app.include_router(user_routes_v1.router, prefix="/api/v1/user", tags=["User v1"])

@app.get("/", tags=["Health"], summary="Health Check")
def root():
    logger.info("Health check accessed.")
    return {"message": "InvoAI User Management API is running 🚀"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_redirect():
    return RedirectResponse(url="/docs")

logger.info("✅ InvoAI API started successfully.")
