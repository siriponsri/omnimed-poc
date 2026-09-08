# SRS Guardian review — source and selected scope

Verdict for source-informed M0 foundation: **PASS with documented scope reductions**. This is a read-only source review; product code and runtime gates are not reviewed here. No finding requires M0 to implement M1–M5. Future schema/closure decisions remain gated as listed below.

Review scope: master prompt, HANDOFF, full SRS extraction and targeted DOCX table-cell verification, and selected mockup source screens. No external clinical/legal standard validity is asserted.

## Findings

### SG-001 — MISSING_INPUT (MEDIUM)

**Evidence:** Master §1; HANDOFF §3; SRS B0008/B0038–B0042.

ai-agent-routing.zip was not supplied in this turn. Source SRS also references ADR-001, ADR-002, SQT Next Account Architecture v2.3, OmniMed DB Schema v1.0 and Project Plan v1.0; none is available in the attachment set.

**Impact:** Cannot claim source-course code reuse, confirmed Next Account adapter contracts, or reconciliation with the historical DB schema.

**Recommended action:** Proceed with M0 under explicit master FastAPI/PostgreSQL/modular-monolith defaults; label four-role control plane as derived from master/HANDOFF only. Request referenced materials only before a future task genuinely depends on them. Never block runnable M0 for absent optional routing code.

**M0 delivery blocker:** No. Future task gates: M0-docs, M1, M3, M5.

### SG-002 — SOURCE_CONTRADICTION (HIGH)

**Evidence:** BR-CORE-12 B0182; BR-CLI-02-02 B0608; US-PHM01-05 B1744.

A revision must set the preceding order status to revoked, while the same rules literally forbid any UPDATE of that order row.

**Impact:** A future Order schema cannot satisfy the literal wording in both directions without an explicit interpretation.

**Recommended action:** Open ADR before M3: order clinical content is immutable; action=REVISE/DISCONTINUE creates a linked new row; only lifecycle state transition on the predecessor is allowed and preserved in append-only lifecycle history. Alternatively represent derived lifecycle as a projection over immutable events. Root must freeze one approach in the contract. Do not change the source quote.

**M0 delivery blocker:** No. Future task gates: M3.

### SG-003 — SELECTED_SLICE_GAP (HIGH)

**Evidence:** BR-CLI-01-03 B0558; BR-CLI-01-04 B0558; VR-CLI-01-03 B0562; VR-CLI-01-01 B0562; VR-CLI-01-08 B0562; Master §3/§10.

SRS encounter completion requires a signed clinical note and exactly one principal diagnosis. The master core demo story does not explicitly include either, and real ICD-10-TM/version and professional-license validation are not established for this POC.

**Impact:** A close endpoint triggered only by dispensing or charge creation would silently violate selected SRS workflow.

**Recommended action:** Keep completion implementation blocked until root freezes a minimal synthetic note/signature/diagnosis decision or an explicit POC deviation. Prefer a future small manually authored note and unambiguously synthetic diagnosis fixture with mock professional identity; never present synthetic codes/signatures as regulated clinical validity. M0 creates no close endpoint.

**M0 delivery blocker:** No. Future task gates: M3, M5.

### SG-004 — POC_SCOPE_AMBIGUITY (HIGH)

**Evidence:** BR-CORE-04 B0157; BR-FIN-02-06 B2141; BR-FIN-02-12 B2141; BR-CORE-19 B0193; Master mandatory exclusions.

SRS distinguishes discharged from completed, allows completed only after account closure, and also requires nonpaying encounters to close by moving debt into receivables. The selected POC does not define payment, receipt, receivable or Next Account behavior.

**Impact:** It is not enough to rename discharged to completed or treat a charge list as paid. The two SRS rules may coexist through a receivable-transfer settlement, but that pathway is not specified for this small demo.

**Recommended action:** Freeze one explicitly synthetic account-settlement path before M5 and record its limitations; do not implement real payment/receivable integration. If not selected, keep encounter clinically discharged and completion task blocked rather than counterfeit zero balance.

**M0 delivery blocker:** No. Future task gates: M5.

### SG-005 — SOURCE_UI_CONFLICT (HIGH)

**Evidence:** BR-ANC01-11 B0977; Mockup HTML line 864; BR-CORE-17 B0193; SRS event catalog B0222/B0224.

Mockup CBC charge source is labeled ปล่อยผล (ANC-01), while the exact lab rule requires charge at analysis technical_complete, expressly before validation/release.

**Impact:** Copying mockup behavior changes charge timing and can duplicate billing when a later result release is handled.

**Recommended action:** SRS wins. Plan lab order.fulfilled at technical_complete as the billable clinical event; result.released changes result availability only. Use idempotent source_event_id charge creation and test no additional charge on release/correction. Record this event timing interpretation before M4.

**M0 delivery blocker:** No. Future task gates: M4.

### SG-006 — LAB_SUBSET_ASSUMPTION (MEDIUM)

**Evidence:** SRS B0948–B0950; US-ANC01-05 B0966; VR-ANC01-07 B0981; Master role/story list.

SRS defines sample → sample_item → analysis → result working layers and requires separate entry/validation actors except for a configured tenant exception. Master has R-LAB but no R-LAB-SUP and supplies only an Hb result for a CBC example.

**Impact:** Directly writing Hb into Observation without traceable performed/released work would bypass LIS semantics; labeling Hb alone as a complete real CBC would overclaim scope.

**Recommended action:** Plan minimal synthetic working records and technical_complete → release transitions. Make the single-operator demo exception explicit; label the panel CBC demo (Hb only), with only Hb marked required. No QC engine, analyzer, accession printer, reflex rule or clinical validity claim.

**M0 delivery blocker:** No. Future task gates: M4.

### SG-007 — AUTHORIZED_DEVIATION (MEDIUM)

**Evidence:** BR-ROLE-02 B0130; NFR-S-01/02 B0256; BR-PLT-01-02 B2905; Master §5/§13.

Production SRS requires database RLS, field encryption and broader IAM; master explicitly permits a starter with future-RLS schema and local POC auth.

**Impact:** An application role selector or application authorization cannot be described as production RLS/PDPA conformance.

**Recommended action:** Use explicit PARTIAL_POC/DEFERRED trace rows; M0 has no protected patient read path. Later routes enforce deny-by-default in application services and tested billing projection boundaries. Production security claims remain deferred.

**M0 delivery blocker:** No. Future task gates: M0, M1, M2, M3, M4, M5.

### SG-008 — AUTHORIZED_DEVIATION (MEDIUM)

**Evidence:** US-CLI-02-03 B0600; US-PHM01-07 B1746; SRS CLI-02 dependencies B0596; Master mandatory out-of-scope list.

Selected ordering modules depend on CLI-08 for clinical safety, while master explicitly excludes CDS/clinical AI. Pharmacy source also requires lot/stock operations, which HANDOFF excludes.

**Impact:** A narrow order/dispense demo has no validated prescribing decision support or inventory integrity.

**Recommended action:** Follow explicit exclusions, constrain to synthetic adult fixed catalog sample, inventory_item_id null, no real-world prescribing or stock claims. Preserve basic structural data validation and manually acknowledged allergy status without adding a CDS engine.

**M0 delivery blocker:** No. Future task gates: M3, M4.

### SG-009 — IDENTITY_AMBIGUITY (MEDIUM)

**Evidence:** US-PAT-01-03 B0301; VR-PAT-01-03/04 B0313; SRS Party/Patient table B0146.

US-PAT-01-03 combines children and anyone lacking a citizen identifier then requires a guardian, whereas VR-PAT-01-04 makes guardian mandatory only for human age <15 and B0146 describes an adult self relation.

**Impact:** The synthetic adult demo intentionally has no real citizen ID; inventing a guardian would distort the identity model.

**Recommended action:** Select adult human Party self relation, generated HN as required identifier under VR-PAT-01-03; do not claim the full US-PAT-01-03 flow. Keep child/unknown-identity/guardian workflows deferred; record assumption rather than silently changing source.

**M0 delivery blocker:** No. Future task gates: M1.

### SG-010 — IDENTIFIER_REFERENCE_DRIFT (LOW)

**Evidence:** SC-ANC01-* B0973; SC-PHM01-* B1751; Mockup HTML lines 458/742/765.

SRS uses US/BR/VR/SC-ANC01-xx and PHM01/PHM02-xx, but mockup writes SC-ANC-01-xx and SC-PHM-01-xx. Some SRS dependencies also call PLT-01 terminology/master-data or PLT-03 master-data, whereas module headings assign Users/RBAC to PLT-01 and Master Data to PLT-02.

**Impact:** Normalizing mockup IDs into the requirement trace would invent SRS IDs; reading dependency labels literally can route work to the wrong platform module.

**Recommended action:** Preserve exact SRS definition IDs, cite B#### locators, treat mockup screen identifiers as presentation aliases only. Derive module ownership from actual module headings and open corrections to source separately.

**M0 delivery blocker:** No. Future task gates: M0-docs, M4.

### SG-011 — REFERENCE_ONLY_UI (LOW)

**Evidence:** Mockup HTML lines 206/229/338/749/750; Master §6.

Mockup contains demonstration KPI numbers, pediatric dose recommendations, and placeholder TMT codes (e.g. TPU 1010xxxx).

**Impact:** Copying these values into the starter would violate the master ban on fake metrics/clinical CDS and create misleading reference data.

**Recommended action:** Reuse clinical layout/spacing/worklist information architecture only. M0 shows module scope/future workflow labels with no synthetic clinical metrics. Later coding uses expressly synthetic local codes or verified standard codes, never placeholder codes presented as standards.

**M0 delivery blocker:** No. Future task gates: M0, M3.

### SG-012 — ROLE_SEMANTIC_BOUNDARY (LOW)

**Evidence:** Role table B0129; BR-PLT-01-01 B2905; BR-FIN-01-12 B2088; Mockup role/navigation arrays.

R-ADM (admission officer) and R-ADMIN (system administrator) are different source roles. SRS requires support-role clinical denial to outrank any additional allowed clinical role.

**Impact:** A permission union or aliasing R-ADM to R-ADMIN can expose clinical content to support/admin users.

**Recommended action:** Seed exactly seven master roles; retain exact IDs. Keep R-ADM out of this OPD starter. Future policy uses explicit deny precedence, tested with mixed-role users as well as ordinary Finance/Admin users.

**M0 delivery blocker:** No. Future task gates: M0, M5.

## Immediate recommendations for root contract freeze

1. Implement M0 only: health/ready, config-only seed, migration infrastructure, Next.js role/navigation shell and deterministic gate scripts. No Patient/Encounter write endpoint is needed to prove M0.
2. Preserve SRS architecture/data definitions in documents without creating full patient/lab/finance schemas prematurely.
3. Freeze explicit POC assumptions listed in PROPOSED_POC_ASSUMPTIONS.md.
4. Attach task gates to SG-002/003/004/005/006 so later Codex tasks cannot silently bypass their decisions.
5. Make TASK M1-01 start with Party/Patient/PatientIdentifier persistence and tests; registration/search UI and encounter workflow follow separate tasks.

## Evidence integrity

- All 53 SRS module titles were extracted from Heading3 paragraphs; dependency lists were not mistaken for additional modules.
- Each of the 153 selected requirement IDs was matched against an actual definition row/paragraph; no missing identifiers and no duplicate IDs in this selected set.
- B#### locators map to the zero-based child index of DOCX w:body and match SRS_EXTRACT.txt.
- Tables preserve exact cell strings. Paragraph quotes preserve exact character text. An editorial pipe joins cells only in CSV/JSON display excerpts.
- Selection status does not imply implementation or SRS-wide compliance.
- Product code, tests and runtime have not been evaluated by this source review.
