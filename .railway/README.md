# Optional Railway authoring

Read ../DEMO_DEPLOYMENT.md first. `railway.ts` describes the entire dedicated demo environment with GitHub source and the product Dockerfiles. `npm ci`, `npm run typecheck`, `npm test` here run offline checks only. No plan/apply or provisioning happens from these checks

Use Railway CLI >=5.42.1, link to `demo`, set OMNIMED_GITHUB_REPOSITORY to the real owner/repository, then review `railway config plan` before `railway config apply`. Never point this file at an existing production environment. Generate a public domain for frontend only after it is healthy

The SDK is tooling, not a runtime dependency. Source push triggers GitHub autodeployment only after service source is linked. Infrastructure changes in this directory require the separate reviewed IaC apply workflow; the supplied CI never applies them
