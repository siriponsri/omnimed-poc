"""Public role names for the navigation preview. These confer no permission."""

from pydantic import BaseModel, ConfigDict


class RolePreview(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    label_th: str
    label_en: str


ROLES = (
    RolePreview(code="R-REG", label_th="เวชระเบียน", label_en="Registration"),
    RolePreview(code="R-SCR", label_th="คัดกรอง", label_en="Screening Nurse"),
    RolePreview(code="R-DOC", label_th="แพทย์", label_en="Doctor"),
    RolePreview(code="R-LAB", label_th="ห้องปฏิบัติการ", label_en="Laboratory"),
    RolePreview(code="R-PHA", label_th="เภสัชกรรม", label_en="Pharmacist"),
    RolePreview(code="R-FIN", label_th="การเงิน", label_en="Finance"),
    RolePreview(code="R-ADMIN", label_th="ตั้งค่าเดโม", label_en="Demo Administration"),
)
