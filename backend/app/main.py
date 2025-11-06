from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api import routes_user, routes_vendor

app = FastAPI(title="InvoAI API", version="1.0")

# Allow frontend (Flask) to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(routes_user.router, prefix="/api/user", tags=["User"])
app.include_router(routes_vendor.router, prefix="/api/vendor", tags=["Vendor"])
