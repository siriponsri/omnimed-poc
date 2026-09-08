"""DATABASE_URL comes only from environment; CLI failures never echo credentials."""

from alembic import context
from alembic.util import CommandError
from sqlalchemy.exc import SQLAlchemyError

from app.config import load_settings
from app.database import build_engine
from app.foundation.models import Base

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    settings = load_settings()
    context.configure(
        url=settings.sqlalchemy_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = build_engine(load_settings())
    try:
        with engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
            )
            with context.begin_transaction():
                context.run_migrations()
    except SQLAlchemyError:
        raise CommandError(
            "PostgreSQL migration failed. Check local database readiness and schema permissions."
        ) from None
    finally:
        engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
