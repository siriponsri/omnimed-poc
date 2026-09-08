from sqlalchemy import inspect

from app.patients.models import Patient, PatientIdentifier, PartyRelation


def test_patient_tables_define_tenant_scoped_invariants() -> None:
    assert {c.name for c in Patient.__table__.constraints} >= {
        "uq_patient_tenant_hn",
        "uq_patient_tenant_id",
        "uq_patient_tenant_party",
    }
    fks = list(inspect(PartyRelation).foreign_key_constraints)
    assert {fk.name for fk in fks} == {
        "fk_party_relation_party",
        "fk_party_relation_related_party",
    }
    assert any(
        i.name == "uq_patient_identifier_preferred" for i in PatientIdentifier.__table__.indexes
    )
