from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    String,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.foundation.models import Base, FixtureAudit

# ruff: noqa: E501


class HnCounter(FixtureAudit, Base):
    __tablename__ = "patient_hn_counter"
    __table_args__ = (ForeignKeyConstraint(["tenant_id"], ["foundation_tenant.id"]),)
    tenant_id: Mapped[UUID] = mapped_column(primary_key=True)
    next_value: Mapped[int] = mapped_column(nullable=False, default=1)


class Party(FixtureAudit, Base):
    __tablename__ = "party"
    __table_args__ = (UniqueConstraint("tenant_id", "id", name="uq_party_tenant_id"),)
    id: Mapped[UUID] = mapped_column(primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(nullable=False)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)


class PartyRelation(FixtureAudit, Base):
    __tablename__ = "party_relation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tenant_id", "party_id"],
            ["party.tenant_id", "party.id"],
            name="fk_party_relation_party",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "related_party_id"],
            ["party.tenant_id", "party.id"],
            name="fk_party_relation_related_party",
        ),
        UniqueConstraint(
            "tenant_id",
            "party_id",
            "related_party_id",
            "relation_type",
            name="uq_party_relation_identity",
        ),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(nullable=False)
    party_id: Mapped[UUID] = mapped_column(nullable=False)
    related_party_id: Mapped[UUID] = mapped_column(nullable=False)
    relation_type: Mapped[str] = mapped_column(String(40), nullable=False)


class Patient(FixtureAudit, Base):
    __tablename__ = "patient"
    __table_args__ = (
        ForeignKeyConstraint(["tenant_id", "party_id"], ["party.tenant_id", "party.id"]),
        UniqueConstraint("tenant_id", "hn", name="uq_patient_tenant_hn"),
        UniqueConstraint("tenant_id", "id", name="uq_patient_tenant_id"),
        UniqueConstraint("tenant_id", "party_id", name="uq_patient_tenant_party"),
    )
    id: Mapped[UUID] = mapped_column(primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(nullable=False)
    party_id: Mapped[UUID] = mapped_column(nullable=False)
    hn: Mapped[str] = mapped_column(String(32), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PatientIdentifier(FixtureAudit, Base):
    __tablename__ = "patient_identifier"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    tenant_id: Mapped[UUID] = mapped_column(nullable=False)
    patient_id: Mapped[UUID] = mapped_column(nullable=False)
    identifier_type: Mapped[str] = mapped_column(String(40), nullable=False)
    value: Mapped[str] = mapped_column(String(120), nullable=False)
    is_preferred: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        ForeignKeyConstraint(["tenant_id", "patient_id"], ["patient.tenant_id", "patient.id"]),
        UniqueConstraint(
            "tenant_id",
            "patient_id",
            "identifier_type",
            "value",
            name="uq_patient_identifier_value",
        ),
        Index(
            "uq_patient_identifier_preferred",
            "tenant_id",
            "patient_id",
            "identifier_type",
            unique=True,
            postgresql_where=(is_preferred == True),
        ),  # noqa: E712
    )
