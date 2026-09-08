"""Transactional patient number allocation."""
# ruff: noqa: E501

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session


def allocate_hn(session: Session, tenant_id: UUID, actor: str, prefix: str = "HN") -> str:
    now = datetime.now(UTC)
    session.execute(
        text("""INSERT INTO patient_hn_counter (tenant_id,next_value,created_at,created_by,updated_at,updated_by)
        VALUES (:t,2,:n,:a,:n,:a) ON CONFLICT (tenant_id) DO UPDATE SET next_value=patient_hn_counter.next_value+1, updated_at=:n, updated_by=:a"""),
        {"t": tenant_id, "n": now, "a": actor},
    )
    value = session.scalar(
        text("SELECT next_value - 1 FROM patient_hn_counter WHERE tenant_id=:t FOR UPDATE"),
        {"t": tenant_id},
    )
    return f"{prefix}-{datetime.now(UTC).year:04d}-{int(value):06d}"
