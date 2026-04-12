import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load variables from .env file
load_dotenv()

# Prefer MYSQL_URL; fallback to constructing from individual vars if needed
MYSQL_URL = os.getenv("MYSQL_URL")
if not MYSQL_URL:
    # Build URL from separate components
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    db = os.getenv("MYSQL_DB")
    MYSQL_URL = f"mysql+asyncmy://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(MYSQL_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
