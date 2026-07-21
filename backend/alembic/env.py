from logging.config import fileConfig
import os
from app.models.police_station import PoliceStation
from app.models.case_assignment import CaseAssignment
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
from app.models.criminal import Criminal
from app.models.case_criminal import CaseCriminal
from app.models.criminal_relation import CriminalRelation
from app.models.evidence_file import EvidenceFile
from app.models.case_activity import CaseActivity
# Load environment variables
load_dotenv()

# Alembic Config object
config = context.config

# Build database URL from .env
DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('DATABASE_USER')}:"
    f"{os.getenv('DATABASE_PASSWORD')}@"
    f"{os.getenv('DATABASE_HOST')}:"
    f"{os.getenv('DATABASE_PORT')}/"
    f"{os.getenv('DATABASE_NAME')}"
)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import Base
from app.database.base import Base

# Import all models so Alembic can discover them
from app.models.user import User
from app.models.officer import Officer
from app.models.case import Case

from app.models.evidence import Evidence


target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in offline mode."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in online mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()