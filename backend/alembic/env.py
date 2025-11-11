from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from dotenv import load_dotenv
import os

from app.models import extracted_json_model

# Load .env
load_dotenv()

from app.core.database import Base
from app.models import user_model, vendor_model, extraction_model, log_model  # import all model files
target_metadata = Base.metadata

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

DATABASE_URL = os.getenv("DATABASE_URL")
DB_SCHEMA = os.getenv("DB_SCHEMA", "invoai")

def run_migrations_online():
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=DB_SCHEMA,
        )
        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        version_table_schema=DB_SCHEMA,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
