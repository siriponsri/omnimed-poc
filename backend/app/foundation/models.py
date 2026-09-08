"""Synthetic foundation fixtures. No patient, credentials, sessions or permissions."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    MetaData,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class FixtureAudit:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by: Mapped[str] = mapped_column(String(64), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_by: Mapped[str] = mapped_column(String(64), nullable=False)


class DemoTenant(FixtureAudit, Base):
    __tablename__ = "foundation_tenant"
    __table_args__ = (
        UniqueConstraint("code"),
        CheckConstraint("synthetic_only = true", name="synthetic_only"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    synthetic_only: Mapped[bool] = mapped_column(Boolean, nullable=False)


class DemoRole(FixtureAudit, Base):
    __tablename__ = "foundation_role"
    __table_args__ = (
        ForeignKeyConstraint(["tenant_id"], ["foundation_tenant.id"], ondelete="RESTRICT"),
    )

    tenant_id: Mapped[UUID] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(16), primary_key=True)
    label_th: Mapped[str] = mapped_column(String(100), nullable=False)
    label_en: Mapped[str] = mapped_column(String(100), nullable=False)


class DemoIdentity(FixtureAudit, Base):
    __tablename__ = "foundation_demo_identity"
    __table_args__ = (
        UniqueConstraint("tenant_id", "fixture_key"),
        ForeignKeyConstraint(["tenant_id"], ["foundation_tenant.id"], ondelete="RESTRICT"),
        ForeignKeyConstraint(
            ["tenant_id", "role_code"],
            ["foundation_role.tenant_id", "foundation_role.code"],
            ondelete="RESTRICT",
        ),
        CheckConstraint("login_enabled = false", name="no_login"),
        CheckConstraint("synthetic_only = true", name="synthetic_only"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(nullable=False)
    fixture_key: Mapped[str] = mapped_column(String(40), nullable=False)
    role_code: Mapped[str] = mapped_column(String(16), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    login_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    synthetic_only: Mapped[bool] = mapped_column(Boolean, nullable=False)
