"""Connection ownership and bounded PostgreSQL readiness checks."""

from collections.abc import Callable
from typing import Literal

from pydantic import BaseModel, Field
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.config import Settings

EXPECTED_REVISION = "0002_patient_persistence"
FOUNDATION_TABLES = (
    "foundation_tenant",
    "foundation_role",
    "foundation_demo_identity",
    "party",
    "patient",
    "patient_identifier",
)


class Readiness(BaseModel):
    status: Literal["ready", "not_ready"]
    database: Literal["reachable", "unavailable"]
    schema_status: Literal["current", "pending", "unknown"] = Field(alias="schema")


Probe = Callable[[], Readiness]


def build_engine(settings: Settings) -> Engine:
    return create_engine(
        settings.sqlalchemy_url,
        pool_pre_ping=True,
        pool_size=3,
        max_overflow=2,
        pool_timeout=3,
        hide_parameters=True,
        connect_args={
            "connect_timeout": 3,
            "options": "-c statement_timeout=3000 -c lock_timeout=3000",
        },
    )


def check_readiness(engine: Engine) -> Readiness:
    """A live database alone is insufficient; the M0 schema must also exist."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            version_table = connection.scalar(text("SELECT to_regclass('public.alembic_version')"))
            if version_table is None:
                return Readiness(status="not_ready", database="reachable", schema="pending")
            revisions = connection.scalars(
                text("SELECT version_num FROM public.alembic_version")
            ).all()
            if revisions != [EXPECTED_REVISION]:
                return Readiness(status="not_ready", database="reachable", schema="pending")
            for table_name in FOUNDATION_TABLES:
                exists = connection.scalar(
                    text("SELECT to_regclass(:relation)"), {"relation": f"public.{table_name}"}
                )
                if exists is None:
                    return Readiness(status="not_ready", database="reachable", schema="pending")
    except SQLAlchemyError:
        # Driver exceptions can include usernames, hostnames, SQL and credentials.
        # Never serialize or log the original exception in a health response.
        return Readiness(status="not_ready", database="unavailable", schema="unknown")
    return Readiness(status="ready", database="reachable", schema="current")
