from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api import routes_user, routes_vendor

app = FastAPI(title="InvoAI API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(routes_user.router, prefix="/api/user", tags=["User"])
app.include_router(routes_vendor.router, prefix="/api/vendor", tags=["Vendor"])
