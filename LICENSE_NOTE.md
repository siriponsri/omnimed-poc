# License and provenance

เอกสาร SRS/UI/HANDOFF ที่ผู้ใช้ให้เป็น project inputs. SRS มีชื่อ Square Tech Solutions Co., Ltd. และไม่มี license grant ที่ยืนยันการเผยแพร่ต่อสาธารณะในรอบนี้. จึง **ยังไม่กำหนด OSS license ให้ repository ทั้งชุด** และไม่อ้างสิทธิ์แทนเจ้าของต้นทาง. การใช้ starter ภายในเพื่อพัฒนาตามคำสั่งผู้ใช้แยกจากการเปิด public repository

โค้ด M0 และเอกสารออกแบบใหม่เขียนสำหรับงานนี้. ไม่คัดลอก source code จาก OpenMRS/Bahmni/OpenELIS/HAPI/agent frameworks/design repos. แนวคิดอ้างอิงและหลักฐาน license อยู่ใน `docs/REFERENCE_AUDIT.md`. ก่อนนำ code ภายนอกมาใช้จริงต้องตรวจ license ที่ file/version นั้นและเก็บ NOTICE ที่จำเป็น

Direct dependencies ใช้ license ของแต่ละแพ็กเกจ: FastAPI/Pydantic/SQLAlchemy/Alembic/pytest/Ruff MIT; Uvicorn/httpx BSD-3-Clause; psycopg LGPL-3.0-only (binary distribution มี bundled dependency obligations); Next.js/React MIT; TypeScript Apache-2.0; Sarabun OFL-1.1. ดู `docs/DEPENDENCIES.md` ซึ่งตรวจ installed metadata จริง ไม่ใช้รายการนี้แทนการตรวจ redistribution obligations ของ container/transitive dependencies

ยังไม่เผยแพร่, ไม่สร้าง fake compliance badge และไม่รับรอง PDPA, ISO, HL7 certification, medical-device หรือ production readiness. Before public release, owner resolves source document redistribution and chooses a license for newly authored work

Sarabun OFL notice คัดลอกจาก installed @fontsource/sarabun/LICENSE แบบไม่แก้ข้อความไว้ที่ frontend/public/licenses/Sarabun-OFL.txt เพื่อให้ติดไปกับ font assets ใน image. ไม่คัดลอก application code จาก reference systems
