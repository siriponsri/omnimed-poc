"""Actual offline PostgreSQL DDL compilation; this is not a live migration pass."""

from io import StringIO
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

ROOT = Path(__file__).resolve().parents[3]


def test_migration_offline_sql_compiles_up_and_down(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://localhost/omnimed_test")
    output = StringIO()
    config = Config(str(ROOT / "db" / "alembic.ini"), output_buffer=output)
    command.upgrade(config, "head", sql=True)
    upgrade_sql = output.getvalue()
    for table in ("foundation_tenant", "foundation_role", "foundation_demo_identity"):
        assert f"CREATE TABLE {table}" in upgrade_sql
    assert "tenant_id UUID NOT NULL" in upgrade_sql
    assert "login_enabled = false" in upgrade_sql
    assert "FOREIGN KEY(tenant_id, role_code)" in upgrade_sql

    output.seek(0)
    output.truncate(0)
    command.downgrade(config, "0001_foundation:base", sql=True)
    downgrade_sql = output.getvalue()
    assert (
        downgrade_sql.index("DROP TABLE foundation_demo_identity")
        < downgrade_sql.index("DROP TABLE foundation_role")
        < downgrade_sql.index("DROP TABLE foundation_tenant")
    )
