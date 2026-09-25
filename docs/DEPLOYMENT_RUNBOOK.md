# Deployment Runbook

## Architecture boundary

Deploy the frontend and backend separately:

- Firebase Hosting may serve the static frontend, preview/staging assets and
  public build metadata.
- Firebase Hosting does not run the Python/FastAPI calculation authority.
- The backend/API needs a separate approved runtime, with server-side secrets,
  reviewed thermo-data version, validation-store access, monitoring and
  allowed origins.

Do not create or guess a Firebase project. Use only the confirmed target and an
authorized login/access path. Never commit tokens, passwords, service-account
private keys or API secrets. A separate Owner approval is not required for the
student team to execute the technical deployment workflow.

## Early and iterative deployment

1. Phase 1: verify local build and status page.
2. Phase 2: verify the confirmed Firebase target, add
   `firebase.json`/`.firebaserc` and deploy the minimum static status page.
   Record URL, project ID and commit after the authorized login/access check.
3. Phase 5: deploy the minimum functional UI after CI passes. Use preview or
   staging if available; keep the backend URL in environment configuration.
4. Phase 9: repeat deployment for hardening smoke tests.
5. Phase 10: production frontend plus separately deployed backend/API.

Automatic production deployment is optional until branch protection, secrets,
runtime ownership and CI gates are confirmed. Never deploy production when
tests fail.

## Release gate

All structure, format, lint, type-check, unit, integration, reference,
validation, build and secret-scan checks must pass. The release must also have
total/partial condenser tests, energy tests, residual tests, API auth tests and
the extrapolation-warning smoke test.

## Production smoke test

Run and record: normal in-range case, extrapolated case, total condenser,
partial condenser, q=1, invalid q, negative heat loss, non-convergent case,
unauthorized API request, energy case and each sensitivity sweep.

Record production URL(s), Firebase project ID, API runtime, commit SHA,
release/version and deployment date. Roll back frontend, API artifact and
scientific data version together when a scientific defect is found.

## Phase 2 static demo procedure

Confirmed target/site: `distillation-simulator` (owner confirmed 2026-09-24).
Install Firebase CLI from the official Firebase distribution (`npm install -g
firebase-tools`; validated with 15.31.0). Run `firebase login` and complete the
browser flow yourself. Never put credentials or CLI auth state in the repo.

1. Check out the intended PR commit and run every README quality check.
2. Require green GitHub PR CI (`CI_REQUIREMENTS.md`).
3. `firebase projects:list` and `firebase hosting:sites:list --project distillation-simulator`.
4. `python scripts/build_frontend.py`.
5. `firebase deploy --only hosting --project distillation-simulator --non-interactive`.
6. Verify HTTPS `/`, `/app.js`, `/styles.css`, `/build-info.json`; compare all
   four response bytes with `build/frontend`. Unknown paths and `/api/health`
   must return 404. Test tabs, reset, validation and the no-calculation state.
7. Record source commit, CI run, build ID, URL, release and verification date.
8. Update PROGRESS/TODO/HANDOVER and push the deployment evidence to the PR.
   Complete the required PR review before merging; do not push directly to
   `main`. The student team may perform the merge/deploy workflow without a
   separate Owner approval step.

Only the four generated public files are deployed. There are no API rewrites,
Functions, databases, credentials or scientific datasets in the Hosting bundle.
Build IDs hash normalized asset bytes and paths, so Windows and Linux produce
the same artifact. Unexpected output files cause build failure; inspect them
before cleanup. The page reports Firebase connection OK only on the confirmed
Hosting domains after public metadata loads; this is static delivery status.

This early DEMO is distinct from the Phase 10 production release gate above.
For rollback, use the Firebase Hosting release history to restore a previously
verified release, or rebuild/redeploy its reviewed commit. Do not disable the
site or modify other Firebase services as a rollback shortcut.

## Latest Phase 2 evidence

Attempt date: 2026-09-25. Source/merge commit:
`bc4d2e5e07451c8d9d8c18e4f23f633fa3e99b52`. GitHub CI run `36154667511` passed.
The production frontend build completed with build ID
`3739c85b7628bc20cd6d5e7aea1bfe42a81a2792beddeb0e5e175c52760cea20`.

Deployment result: `firebase deploy --only hosting --project
distillation-simulator --non-interactive` failed before upload because the
current authorized CLI session could not access the target project; Firebase
returned a project-access/HTTP 403 error. Production URL and smoke-test result:
not available. Phase 2 remains `BLOCKED`; do not record `DONE` until access,
deployment and smoke verification succeed.
