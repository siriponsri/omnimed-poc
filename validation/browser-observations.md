# Browser observation record

Scope: actual cloud-browser manual interaction with the Next.js development preview before packaging; desktop viewport 1363×936. This is not the automated Playwright suite and not a Docker or Railway deployment test

Observed on 2026-09-08:

- Thai registration worklist rendered with M0/synthetic banner, seven-role selector, real empty state and disabled registration action. No fake patients/metrics. Screenshot inspected for readable Thai font, contrast and clinical worklist layout
- Selecting R-FIN updated heading to รายการค่าใช้จ่าย and table to account/HN/amount/status; no clinical patient header; View charges remained disabled
- Switching EN updated html lang=en, Encounter charges heading and English navigation/copy. Selecting R-DOC updated heading to OPD consulting room and showed empty patient context
- Foundation status button changed the panel. Check again moved Not checked → Checking → Not ready when the backend/database path was unavailable; button re-enabled. No driver error/DSN displayed
- DOM measurement: documentElement.scrollWidth=1363, innerWidth=1363; no horizontal document overflow at observed desktop width

Initial dev-preview interaction did not hydrate through the preview hostname. Adding terminal.local to Next allowedDevOrigins and reloading restored state changes. This setting applies to development only; no clinical authorization is implied. The final build subsequently passed. Later copy-only change renamed Local connection to Connection status

Exact 1366×768 automation, mobile 390px and keyboard scenarios are supplied in tests/e2e/foundation.spec.ts but their automated execution remains NOT_RUN. No keyboard/mobile PASS is inferred from source inspection or desktop screenshot. Preview was not published and is stopped
