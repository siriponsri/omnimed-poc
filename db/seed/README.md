# M0 synthetic fixtures

รันจาก repository root หลัง `alembic -c db/alembic.ini upgrade head`:

```bash
uv run python scripts/seed_demo.py
```

คำสั่งอ่าน `DATABASE_URL` และ `APP_ENV=local|test` จาก environment และทำงานใน PostgreSQL transaction เดียว Seed สร้าง tenant สมมุติ 1 ราย, role labels 7 รายการ และ identity fixtures 7 รายการโดยใช้ UUID/timestamp คงที่ ไม่มี patient rows, password, login หรือ permission grants

เรียกซ้ำแล้วข้อมูลเดิมไม่เปลี่ยน ถ้าข้อมูล fixture ถูกแก้แล้ว seed จะยกเลิก transaction แทนการเขียนทับ ข้อมูล fixtures อยู่ที่ `backend/app/foundation/seed.py`; role labels ใช้ `backend/app/foundation/catalog.py`

ตาราง `foundation_*` เป็นข้อมูลประกอบ M0 ไม่ใช่ implementation ของ SRS User/Role/IAM ระบบ authorization และ audit ที่ใช้ข้อมูลผู้ป่วยต้องมี task contract ก่อนเริ่ม M1
