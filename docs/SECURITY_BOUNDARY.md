# Security boundary

M0 operates on synthetic configuration only. It is not production IAM, PDPA/RLS/encryption conformance or a clinical system

## Implemented now

- No patient, Encounter, clinical, billing or authenticated read endpoints. Only public liveness/readiness/foundation metadata
- Unknown routes have no permissions or behavior; forged role header cannot unlock a clinical path because no such path exists
- Role selector explicitly previews navigation; foundation demo identities have no credentials or sessions
- Env-only database secret, generated locally; .env excluded from Git/build context/ZIP. No hard-coded API key. OpenRouter has no live implementation
- Readiness 503 on database/schema failure; sanitized public errors. API docs UI disabled (no CDN requirement). SQL echo and HTTP access logs disabled in documented backend start
- Docker ports loopback only, app containers non-root; no frontend cloud font or API dependency

## Scaffolded / required with first protected route

Application auth with server-derived actor + tenant, role permission mapping, default deny, and audited disclosure. M1 identity APIs must implement these before patient data is exposed; do not wait for M5. Protected audit write and read should share one transaction where practical; if recording access fails, return no protected payload. Audit metadata identifies actor/time/context/resource/outcome, never duplicates sensitive bodies into logs

| Principal | Identity | Clinical details | Billing | Configuration |
|---|---|---|---|---|
| R-REG | bounded read/write | deny | deny | deny |
| R-SCR | required context | assigned triage subset | deny | deny |
| R-DOC | assigned context | assigned encounter/orders | deny | deny |
| R-LAB | necessary IDs | assigned section/results only | deny | deny |
| R-PHA | necessary IDs | medication work subset | deny | deny |
| R-FIN | billing IDs only | deny | allowed projection | deny |
| R-ADMIN | demo account metadata | deny | deny | allowed subset |

Table is a target policy, not implemented RBAC. Support-role deny wins for mixed-role identities; R-ADMIN is not a superuser. Test object-level/tenant-level authorization as well as role checks. Never authorize from a query parameter, UI tab, localStorage or X-Demo-Role header

## Deferred production requirements

PostgreSQL RLS, least-privilege DB users per purpose, pgcrypto field encryption, managed key lifecycle, real password/session/SSO/MFA, transport TLS, break-glass, audit tamper protection/retention, consent/legal policy, rate limiting and operational backups/DR. BR-ROLE-02 database enforcement is explicitly PARTIAL_POC under master authorization

## Known limits and local behavior

Database credentials grant local POC database privileges and are not tenant/RLS isolation. HTTP on loopback is local development only. Docker Desktop installation depends on the host's policy; do not bypass workplace restrictions. First package/image download needs network; subsequent runtime uses local services only. No synthetic fixture should be replaced with real records in this starter

## Future negative cases

Unauthenticated read denied; R-FIN/R-ADMIN clinical read denied (including mixed roles); wrong tenant/section/object denied; denied attempt audited without leaking target existence; malformed dosage/observation data rejected; revoked order cannot dispense; audit failure denies disclosure; secrets absent from UI/trace/error logs. M5 consolidates tests but does not postpone these controls
