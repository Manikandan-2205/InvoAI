# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # --- App Meta ---
    APP_NAME: str = Field("InvoAI User Management", description="FastAPI App Name")
    APP_VERSION: str = Field("1.0.0", description="App Version")

    # --- Database ---
    DATABASE_URL: str = Field(..., description="SQLAlchemy DB URL")
    DB_SCHEMA: str = Field("invoai", description="Database Schema")

    # --- Logging / Environment ---
    LOG_LEVEL: str = Field("INFO", description="App log level")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
