# OmniMed SRS module inventory — proposed scope classification

Source: OmniMed SRS v2.0, exact Heading3 module identifiers and titles. Status describes the planned M0–M5 selected subset; it is not implementation completion. Master §20 restricts this delivery to M0.

| Module | Source | Scope | Milestone | Selected boundary / reason |
|---|---|---|---|---|
| PAT-01 · ทะเบียนผู้ป่วยและดัชนีตัวตนกลาง (Patient Registry & Master Patient Index) | B0286 | IN_SCOPE | M1 | Adult synthetic Party/Patient, self relation, HN and PatientIdentifier; search/register only. No MPI merge, national ID/card reader, animal or child registration. |
| PAT-02 · คัดกรองและระบบคิว (Screening & Queue Management) | B0335 | IN_SCOPE | M1/M2 | AMB encounter and triage/vital Observations. Queue remains workflow context; no public kiosk, live queue operations, acuity CDS. |
| PAT-03 · นัดหมายและตารางเวรแพทย์ (Appointment & Provider Scheduling) | B0384 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| PAT-04 · สิทธิการรักษาและการตรวจสอบสิทธิ (Coverage & Eligibility) | B0433 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| PAT-05 · ส่งต่อผู้ป่วย (Patient Referral) | B0482 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| CLI-01 · เวชระเบียนอิเล็กทรอนิกส์ (Electronic Medical Record) | B0535 | IN_SCOPE | M2/M3/M5 | Doctor read view of current vital/lab Observations; minimal signing/diagnosis for completion is unresolved in finding SG-003. |
| CLI-02 · ห้องตรวจแพทย์และการสั่งการรักษา (Consultation & CPOE) | B0585 | IN_SCOPE | M3 | Doctor workspace, lab and medication orders, lifecycle/revision only. CDS, order sets, IPD disposition and verbal orders excluded. |
| CLI-03 · ทันตกรรม (Dentistry) | B0635 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| CLI-04 · อุบัติเหตุ-ฉุกเฉิน (Emergency Department) | B0685 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| CLI-05 · ตรวจสุขภาพและลูกค้าองค์กร (Health Check-up & Corporate Clients) | B0735 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| CLI-06 · วัคซีน (Immunization) | B0785 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| CLI-07 · กราฟการเจริญเติบโตและพัฒนาการ (Growth Charts & Developmental Screening) | B0841 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| CLI-08 · ระบบสนับสนุนการตัดสินใจทางคลินิก (Clinical Decision Support) | B0890 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| ANC-01 · ห้องปฏิบัติการ (Laboratory Information System — LIS) | B0944 | IN_SCOPE | M4 | Manual synthetic CBC/Hemoglobin lab worklist/result, minimum working-layer trace, technical_complete charge and result release. No analyzer/QC automation/reflex. |
| ANC-02 · รังสีวิทยา (Radiology Information System + PACS Integration) | B1013 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| ANC-03 · ธนาคารเลือด (Blood Bank) | B1077 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| IPD-01 · ADT และผังเตียง (Admission, Discharge, Transfer & Bed Board) | B1142 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| IPD-02 · หอผู้ป่วยในและบันทึกทางการพยาบาล (Inpatient Ward & Nursing Documentation) | B1206 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| IPD-03 · หอผู้ป่วยวิกฤตและทารกแรกเกิด (ICU & Neonatal Care) | B1264 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| IPD-04 · บริหารยาข้างเตียง (Electronic Medication Administration Record — eMAR) | B1325 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| IPD-05 · โภชนาการ (Clinical Nutrition & Food Service) | B1386 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| PER-01 · ห้องผ่าตัด (Operating Theatre Management) | B1450 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| PER-02 · วิสัญญี (Anaesthesia) | B1519 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| PER-03 · ฝากครรภ์และห้องคลอด (Antenatal Care & Labour/Delivery) | B1585 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| PER-04 · ไตเทียม (Haemodialysis) | B1651 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| PHM-01 · สั่งยาและใบสั่งยา (Medication Ordering / CPOE) | B1725 | IN_SCOPE | M3 | Fixed adult synthetic Paracetamol 500 mg order, structured order_detail, revision. No safety engine or clinical dosing recommendation. |
| PHM-02 · ห้องยาและการจ่ายยา (Pharmacy Dispensing) | B1787 | IN_SCOPE | M4 | OPD active-order dispensing with actor/time/quantity and medication.dispensed event. No stock/lot, controlled substances, returns or unit dose. |
| PHM-03 · คลังยาและเวชภัณฑ์ (Pharmacy & Medical Supply Inventory) | B1853 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| PHM-04 · จัดซื้อเวชภัณฑ์ (Medical Procurement) | B1923 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| PHM-05 · เวชภัณฑ์ปลอดเชื้อ CSSD (Central Sterile Supply Department) | B1988 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| FIN-01 · บันทึกค่าใช้จ่าย (Charge Capture) | B2065 | IN_SCOPE | M4 | Event-derived charges, price snapshot, safe billing labels, source event/order trace. |
| FIN-02 · การเงินและใบเสร็จ (Cashiering & Receipting) | B2118 | IN_SCOPE | M4/M5 | Finance charge read projection and eventual synthetic encounter-account completion only; completion/payment semantics unresolved SG-004. No real receipt/payment integration. |
| FIN-03 · ผังราคาและแพ็กเกจ (Chargemaster & Packages) | B2166 | IN_SCOPE | M4 | Fixed synthetic default charge definitions with currency/price validity. No price manager, packages, payer price rules or approval workflow. |
| FIN-04 · เชื่อมบัญชีแยกประเภท (General Ledger Integration) | B2214 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| THA-01 · รหัสมาตรฐานไทย (Thai Terminology Service) | B2273 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| THA-02 · ส่งออก 43 แฟ้ม → HDC (43-File Export to Health Data Center) | B2322 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| THA-03 · e-Claim สปสช. (NHSO e-Claim) | B2371 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| THA-04 · ประกันสังคม (Social Security Office — SSOP / AIPN) | B2421 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| THA-05 · กรมบัญชีกลาง (Comptroller General’s Department — CSMBS) | B2471 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| THA-06 · Thai DRG Grouper (Thai Diagnosis Related Groups) | B2520 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| THA-07 · หมอพร้อม / MOPH Refer / Health Link (National Health Data Exchange) | B2569 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| DIG-01 · พอร์ทัลผู้ป่วยและ LINE OA (Patient Portal & LINE OA) | B2637 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| DIG-02 · โทรเวชกรรมและใบสั่งยาอิเล็กทรอนิกส์ (Telemedicine & e-Prescription) | B2686 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| DIG-03 · คิวดิจิทัล จอเรียกคิว และ Kiosk (Digital Queue, Display & Kiosk) | B2734 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| DIG-04 · ระบบสร้างแรงจูงใจสำหรับเด็ก (Gamification) | B2782 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| DIG-05 · ผู้ช่วยปัญญาประดิษฐ์ (AI Assist) | B2830 | OUT_OF_SCOPE | — | Excluded by master/HANDOFF mandatory scope: no product implementation or external runtime dependency. |
| PLT-01 · ผู้ใช้และการควบคุมสิทธิ์ (Users & RBAC) | B2882 | IN_SCOPE | M0/M5 | Seven role definitions/config in M0; deny-by-default local application authorization in later features. Production IAM/RLS deferred. |
| PLT-02 · ข้อมูลหลักและตัวจัดการ Specialty Pack (Master Data & Specialty Pack Manager) | B2930 | IN_SCOPE | M0/M2/M3 | Minimal demo metadata seed; later ObservationDefinition/CatalogItem. Specialty Pack installation and master-data administration deferred. |
| PLT-03 · เครื่องยนต์ฟอร์มและแม่แบบ (Form / Template Engine) | B2978 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| PLT-04 · PDPA — ความยินยอม การตรวจสอบ และสิทธิ์เจ้าของข้อมูล (Consent, Audit, DSAR) | B3027 | IN_SCOPE | M0/M5 | Audit contract in M0; protected read/disclosure evidence for implemented future routes. No consent/DSAR/legal compliance or immutable retention guarantee. |
| PLT-05 · FHIR และ Open API (FHIR & Open API) | B3078 | IN_SCOPE | M0/M5 | R4 mapping boundary document in M0; minimal local read/export later. No full FHIR server, external clients, SMART, bulk export or inbound writes. |
| PLT-06 · รายงานและระบบวิเคราะห์ (Reports & BI) | B3126 | DEFERRED | After selected POC; requires a new task/contract | Not needed to prove the selected OPD path; no implementation in M0–M5 contract. |
| PLT-07 · การตั้งค่าระบบและหลายผู้เช่า (System Settings & Multi-tenant) | B3175 | IN_SCOPE | M0/M5 | Single-tenant local configuration, migration/health and reference-only transactional outbox scaffold. No multi-tenant production operation/DR/HA. |

Counts: DEFERRED = 12, IN_SCOPE = 15, OUT_OF_SCOPE = 26.
