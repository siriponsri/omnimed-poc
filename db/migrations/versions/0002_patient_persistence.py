"""Party, patient and tenant scoped identifiers."""
from alembic import op
import sqlalchemy as sa
revision="0002_patient_persistence"; down_revision="0001_foundation"; branch_labels=None; depends_on=None
def audit(): return [sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.Column("created_by",sa.String(64),nullable=False),sa.Column("updated_at",sa.DateTime(timezone=True),nullable=False),sa.Column("updated_by",sa.String(64),nullable=False)]
def upgrade():
 op.create_table("patient_hn_counter",sa.Column("tenant_id",sa.Uuid(),primary_key=True),sa.Column("next_value",sa.Integer(),nullable=False),*audit(),sa.ForeignKeyConstraint(["tenant_id"],["foundation_tenant.id"]))
 op.create_table("party",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("tenant_id",sa.Uuid(),nullable=False),sa.Column("display_name",sa.String(200),nullable=False),*audit(),sa.UniqueConstraint("tenant_id","id"))
 op.create_table("party_relation",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("tenant_id",sa.Uuid(),nullable=False),sa.Column("party_id",sa.Uuid(),nullable=False),sa.Column("related_party_id",sa.Uuid(),nullable=False),sa.Column("relation_type",sa.String(40),nullable=False),*audit(),sa.ForeignKeyConstraint(["tenant_id","party_id"],["party.tenant_id","party.id"]),sa.ForeignKeyConstraint(["tenant_id","related_party_id"],["party.tenant_id","party.id"]),sa.UniqueConstraint("tenant_id","party_id","related_party_id","relation_type"))
 op.create_table("patient",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("tenant_id",sa.Uuid(),nullable=False),sa.Column("party_id",sa.Uuid(),nullable=False),sa.Column("hn",sa.String(32),nullable=False),sa.Column("date_of_birth",sa.DateTime(timezone=True),nullable=False),*audit(),sa.ForeignKeyConstraint(["tenant_id","party_id"],["party.tenant_id","party.id"]),sa.UniqueConstraint("tenant_id","hn"))
 op.create_table("patient_identifier",sa.Column("id",sa.Uuid(),primary_key=True),sa.Column("tenant_id",sa.Uuid(),nullable=False),sa.Column("patient_id",sa.Uuid(),nullable=False),sa.Column("identifier_type",sa.String(40),nullable=False),sa.Column("value",sa.String(120),nullable=False),sa.Column("is_preferred",sa.Boolean(),nullable=False),*audit(),sa.ForeignKeyConstraint(["tenant_id","patient_id"],["patient.tenant_id","patient.id"]),sa.UniqueConstraint("tenant_id","patient_id","identifier_type","value"))
 op.execute("CREATE UNIQUE INDEX uq_patient_identifier_preferred ON patient_identifier (tenant_id, patient_id, identifier_type) WHERE is_preferred")
def downgrade():
 op.drop_index("uq_patient_identifier_preferred",table_name="patient_identifier"); op.drop_table("patient_identifier"); op.drop_table("patient"); op.drop_table("party_relation"); op.drop_table("party"); op.drop_table("patient_hn_counter")
