from logging.config import fileConfig
import os
from urllib.parse import urlparse, urlunparse
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from dotenv import load_dotenv
import pymysql

from app.models import extracted_json_model

# Load .env variables
load_dotenv()

# Get MySQL URL (may include DB name)
MYSQL_URL = os.getenv("MYSQL_URL")
if not MYSQL_URL:
    raise RuntimeError("MYSQL_URL not set in .env")

# Parse URL to extract components
parsed = urlparse(MYSQL_URL)
# If database part is missing, raise error later
if not parsed.path or parsed.path == "/":
    raise RuntimeError("MYSQL_URL must include a database name, e.g., mysql+pymysql://user:pass@host:port/db")

# Build a URL without the database for creation check
creation_url = urlunparse((parsed.scheme, parsed.netloc, "/", parsed.params, parsed.query, parsed.fragment))

# Ensure the database exists (create if not)
conn = pymysql.connect(host=parsed.hostname, port=parsed.port or 3306, user=parsed.username, password=parsed.password)
try:
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{parsed.path.lstrip('/')}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.commit()
finally:
    conn.close()

# Use the full URL for migrations
DATABASE_URL = MYSQL_URL

from app.core.database import Base
from app.models import user_model, vendor_model, extraction_model, log_model  # import all model files
target_metadata = Base.metadata

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use the URL from env for migrations
def run_migrations_online():
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=os.getenv("DB_SCHEMA", "public"),
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    raise RuntimeError("Offline mode not supported for MySQL migrations")
else:
    run_migrations_online()
