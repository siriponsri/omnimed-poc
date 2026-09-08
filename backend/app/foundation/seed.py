"""Deterministic, transactional M0 fixtures. Existing fixture content is not overwritten."""

from datetime import UTC, datetime
from typing import cast
from uuid import UUID, uuid5

from pydantic import BaseModel
from sqlalchemy import Connection, Engine, Table, select, text
from sqlalchemy.dialects.postgresql import insert

from app.database import EXPECTED_REVISION
from app.foundation.catalog import ROLES
from app.foundation.models import DemoIdentity, DemoRole, DemoTenant

SEED_NAMESPACE = UUID("117edc75-064e-4a24-acf3-47a3f7d0c69d")
TENANT_ID = uuid5(SEED_NAMESPACE, "omnimed-synthetic-demo")
FIXTURE_TIME = datetime(2026, 9, 8, 0, 0, tzinfo=UTC)
FIXTURE_ACTOR = "system:m0-fixture-v1"


class SeedConflict(RuntimeError):
    """Refuse to silently mutate a fixture with unexpected contents."""


class SeedSummary(BaseModel):
    fixture_version: str = "m0-v1"
    tenants: int = 1
    roles: int = 7
    identities: int = 7
    login_enabled: bool = False


def _audit_fields() -> dict[str, object]:
    return {
        "created_at": FIXTURE_TIME,
        "created_by": FIXTURE_ACTOR,
        "updated_at": FIXTURE_TIME,
        "updated_by": FIXTURE_ACTOR,
    }


def fixture_records() -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    tenant: dict[str, object] = {
        "id": TENANT_ID,
        "code": "SYNTHETIC-DEMO",
        "display_name": "OmniMed Synthetic Demo",
        "synthetic_only": True,
        **_audit_fields(),
    }
    roles: list[dict[str, object]] = []
    identities: list[dict[str, object]] = []
    for role in ROLES:
        roles.append({"tenant_id": TENANT_ID, **role.model_dump(), **_audit_fields()})
        identities.append(
            {
                "id": uuid5(SEED_NAMESPACE, role.code),
                "tenant_id": TENANT_ID,
                "fixture_key": f"demo-{role.code.removeprefix('R-').lower()}",
                "role_code": role.code,
                "display_name": f"Synthetic {role.label_en}",
                "login_enabled": False,
                "synthetic_only": True,
                **_audit_fields(),
            }
        )
    return tenant, roles, identities


def _insert_and_verify(
    connection: Connection,
    model: type[DemoTenant] | type[DemoRole] | type[DemoIdentity],
    records: list[dict[str, object]],
) -> None:
    table = cast(Table, model.__table__)
    for expected in records:
        connection.execute(insert(table).values(**expected).on_conflict_do_nothing())
        query = select(table)
        for column in table.primary_key.columns:
            query = query.where(column == expected[column.name])
        actual = connection.execute(query).mappings().one_or_none()
        if actual is None or any(actual[key] != value for key, value in expected.items()):
            raise SeedConflict("Unexpected M0 fixture content; seed transaction rolled back.")


def seed_demo(engine: Engine) -> SeedSummary:
    if engine.dialect.name != "postgresql":
        raise SeedConflict("M0 seed requires PostgreSQL.")
    # The caller explicitly invokes seeding; a transaction keeps all fixture writes atomic.
    with engine.begin() as connection:
        revision = connection.scalars(text("SELECT version_num FROM public.alembic_version")).all()
        if revision != [EXPECTED_REVISION]:
            raise SeedConflict("Migrate the M0 schema before seeding.")
        tenant, roles, identities = fixture_records()
        _insert_and_verify(connection, DemoTenant, [tenant])
        _insert_and_verify(connection, DemoRole, roles)
        _insert_and_verify(connection, DemoIdentity, identities)
    return SeedSummary()
