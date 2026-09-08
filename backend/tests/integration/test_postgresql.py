"""Opt in with an EMPTY disposable database named omnimed_test or omnimed_test_*.

OMNIMED_TEST_DATABASE_URL=postgresql+psycopg://.../omnimed_test uv run pytest \
    backend/tests/integration -q

Tests refuse existing public tables; they never substitute SQLite or touch the demo database.
"""

import os
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy import inspect, select, text, update
from sqlalchemy.exc import IntegrityError

from app.config import Settings
from app.database import FOUNDATION_TABLES, build_engine, check_readiness
from app.foundation.models import Base, DemoIdentity, DemoRole, DemoTenant
from app.foundation.seed import SeedConflict, fixture_records, seed_demo
from app.main import create_app
from app.patients import models  # noqa: F401

pytestmark = pytest.mark.integration
ROOT = Path(__file__).resolve().parents[3]


def test_postgresql_migration_seed_and_tenant_constraints(monkeypatch: pytest.MonkeyPatch) -> None:
    dsn = os.getenv("OMNIMED_TEST_DATABASE_URL")
    if not dsn:
        pytest.skip("Set OMNIMED_TEST_DATABASE_URL to an empty disposable PostgreSQL database")
    settings = Settings(app_env="test", database_url=SecretStr(dsn))
    name = settings.sqlalchemy_url.database or ""
    if name != "omnimed_test" and not name.startswith("omnimed_test_"):
        pytest.fail("Integration tests require a disposable database named omnimed_test[_suffix]")
    engine = build_engine(settings)
    try:
        if inspect(engine).get_table_names(schema="public"):
            pytest.fail("Integration tests refuse existing public tables; use an empty test DB")
        monkeypatch.setenv("APP_ENV", "test")
        monkeypatch.setenv("DATABASE_URL", dsn)
        config = Config(str(ROOT / "db" / "alembic.ini"))
        assert check_readiness(engine).schema_status == "pending"

        command.upgrade(config, "head")
        assert check_readiness(engine).status == "ready"
        assert set(inspect(engine).get_table_names()) == {*FOUNDATION_TABLES, "alembic_version"}
        with engine.connect() as connection:
            context = MigrationContext.configure(connection, opts={"compare_type": True})
            assert compare_metadata(context, Base.metadata) == []

        command.downgrade(config, "base")
        assert set(inspect(engine).get_table_names()) == {"alembic_version"}
        assert check_readiness(engine).status == "not_ready"
        command.upgrade(config, "head")

        first = seed_demo(engine)
        with engine.connect() as connection:
            snapshot = connection.execute(
                select(DemoIdentity.__table__).order_by(DemoIdentity.id)
            ).all()
        second = seed_demo(engine)
        with engine.connect() as connection:
            assert (
                connection.execute(select(DemoIdentity.__table__).order_by(DemoIdentity.id)).all()
                == snapshot
            )
            assert connection.scalar(text("SELECT count(*) FROM foundation_tenant")) == 1
            assert connection.scalar(text("SELECT count(*) FROM foundation_role")) == 7
            assert connection.scalar(text("SELECT count(*) FROM foundation_demo_identity")) == 7
        assert first == second

        _, _, identity_records = fixture_records()
        with pytest.raises(IntegrityError), engine.begin() as connection:
            connection.execute(update(DemoIdentity).values(login_enabled=True))
        # A tenant must not borrow another tenant's role, even when both tenants exist.
        tenant_record, _, _ = fixture_records()
        other_tenant_id = uuid4()
        with engine.begin() as connection:
            connection.execute(
                DemoTenant.__table__.insert().values(
                    **{**tenant_record, "id": other_tenant_id, "code": "SYNTHETIC-SECOND"}
                )
            )
        with pytest.raises(IntegrityError), engine.begin() as connection:
            connection.execute(
                DemoIdentity.__table__.insert().values(
                    **{**identity_records[0], "id": uuid4(), "tenant_id": other_tenant_id}
                )
            )

        with engine.begin() as connection:
            connection.execute(update(DemoRole).values(label_en="unexpected-edit"))
        with pytest.raises(SeedConflict):
            seed_demo(engine)

        with TestClient(create_app(settings=settings)) as client:
            assert client.get("/api/health/live").status_code == 200
            assert client.get("/api/health/ready").status_code == 200

        command.downgrade(config, "base")
        with engine.begin() as connection:
            connection.execute(text("DROP TABLE alembic_version"))
        assert inspect(engine).get_table_names() == []
    finally:
        engine.dispose()
