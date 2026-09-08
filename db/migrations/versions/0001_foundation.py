"""Synthetic tenant and role fixtures; no clinical data or authentication.

Revision ID: 0001_foundation
Revises: None
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_foundation"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _audit_columns() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.String(64), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_by", sa.String(64), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "foundation_tenant",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(40), nullable=False),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("synthetic_only", sa.Boolean(), nullable=False),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_foundation_tenant")),
        sa.UniqueConstraint("code", name=op.f("uq_foundation_tenant_code")),
        sa.CheckConstraint(
            "synthetic_only = true", name=op.f("ck_foundation_tenant_synthetic_only")
        ),
    )
    op.create_table(
        "foundation_role",
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(16), nullable=False),
        sa.Column("label_th", sa.String(100), nullable=False),
        sa.Column("label_en", sa.String(100), nullable=False),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("tenant_id", "code", name=op.f("pk_foundation_role")),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["foundation_tenant.id"],
            name=op.f("fk_foundation_role_tenant_id_foundation_tenant"),
            ondelete="RESTRICT",
        ),
    )
    op.create_table(
        "foundation_demo_identity",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("fixture_key", sa.String(40), nullable=False),
        sa.Column("role_code", sa.String(16), nullable=False),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("login_enabled", sa.Boolean(), nullable=False),
        sa.Column("synthetic_only", sa.Boolean(), nullable=False),
        *_audit_columns(),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_foundation_demo_identity")),
        sa.UniqueConstraint(
            "tenant_id", "fixture_key", name=op.f("uq_foundation_demo_identity_tenant_id")
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["foundation_tenant.id"],
            name=op.f("fk_foundation_demo_identity_tenant_id_foundation_tenant"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id", "role_code"],
            ["foundation_role.tenant_id", "foundation_role.code"],
            name=op.f("fk_foundation_demo_identity_tenant_id_foundation_role"),
            ondelete="RESTRICT",
        ),
        sa.CheckConstraint(
            "login_enabled = false", name=op.f("ck_foundation_demo_identity_no_login")
        ),
        sa.CheckConstraint(
            "synthetic_only = true", name=op.f("ck_foundation_demo_identity_synthetic_only")
        ),
    )


def downgrade() -> None:
    # M0 fixtures contain no clinical records. Future clinical migrations need their own review.
    op.drop_table("foundation_demo_identity")
    op.drop_table("foundation_role")
    op.drop_table("foundation_tenant")
