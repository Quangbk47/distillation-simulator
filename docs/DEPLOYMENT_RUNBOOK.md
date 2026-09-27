# Deployment Runbook

## Architecture boundary

Deploy the frontend and backend separately:

- Firebase Hosting may serve the static frontend, preview/staging assets and
  public build metadata.
- Firebase Hosting does not run the Python/FastAPI calculation authority.
- The backend/API needs a separate selected runtime, with server-side secrets,
  reviewed thermo-data version, validation-store access, monitoring and
  allowed origins.

The student team may use its own Firebase account and may create, select or
replace a Firebase project/site when needed. Update `.firebaserc`,
`firebase.json`, `PROGRESS.md`, `TODO.md` and `HANDOVER.md` with the resulting
project/site and real production URL. Never commit tokens, passwords,
service-account private keys or API secrets. Owner approval is not required for
this technical deployment workflow.

## Early and iterative deployment

1. Phase 1: verify local build and status page.
2. Phase 2: use or create a student-controlled Firebase target, add/update
   `firebase.json`/`.firebaserc` and deploy the minimum static status page.
   Record URL, project ID/site and commit after the public smoke test.
3. Phase 5: deploy the minimum functional UI after CI passes. Use preview or
   staging if available; keep the backend URL in environment configuration.
4. Phase 9: repeat deployment for hardening smoke tests.
5. Phase 10: production frontend plus separately deployed backend/API.

Automatic production deployment is optional until CI/deployment automation is
ready. The student team may configure it. Never deploy production when tests
fail.

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

Current verified target/site: `distillation-simulator`. Access was reverified
on 2026-09-27 and deployment succeeded. Reuse this target while accessible;
authorized replacement remains an option only when needed. Keep credentials
outside the repository. Use the existing Firebase CLI and authorized login profile.

1. Check out the intended PR commit and run every README quality check.
2. Require green GitHub PR CI (`CI_REQUIREMENTS.md`).
3. Run `firebase projects:list`. Use an accessible student project/site or
   create one in Firebase Console/CLI; record the selected project ID/site.
4. Update `.firebaserc` and `firebase.json` to that project/site; validate the
   diff contains no credential or secret.
5. `firebase hosting:sites:list --project <project-id>` and
   `python scripts/build_frontend.py`.
6. `firebase deploy --only hosting --project <project-id> --non-interactive`.
7. Verify HTTPS `/`, `/app.js`, `/styles.css`, `/build-info.json`; compare all
   four response bytes with `build/frontend`. Unknown paths and `/api/health`
   must return 404. Test tabs, reset, validation and the no-calculation state.
8. Record source commit, CI run, build ID, real URL, release and verification date.
9. Update PROGRESS/TODO/HANDOVER and push the deployment evidence to the PR.
   Complete the required PR review before merging; do not push directly to
   `main`. The student team may perform the merge/deploy workflow without a
   separate Owner approval step.

Only the four generated public files are deployed. There are no API rewrites,
Functions, databases, credentials or scientific datasets in the Hosting bundle.
Build IDs hash normalized asset bytes and paths, so Windows and Linux produce
the same artifact. Unexpected output files cause build failure; inspect them
before cleanup. The page reports Firebase connection OK only on the selected
Hosting domains after public metadata loads; this is static delivery status.

This early DEMO is distinct from the Phase 10 production release gate above.
For rollback, use the Firebase Hosting release history to restore a previously
verified release, or rebuild/redeploy its reviewed commit. Do not disable the
site or modify other Firebase services as a rollback shortcut.

## Latest Phase 2 evidence

- Verified: 2026-09-27.
- Source: `f09b299200cfec94c85139a97c4a98d0cc2a946f` (main, PR #5 merge).
- CI: https://github.com/Quangbk47/distillation-simulator/actions/runs/36157068321
  — completed, success.
- Local gate: structure, format, lint, mypy, 13 tests, frontend/package builds
  passed; detect-secrets reported zero findings. TestClient emitted one upstream
  deprecation warning; no failures.
- Project/site: `distillation-simulator` (project number `654072668208`).
- URL: https://distillation-simulator.web.app.
- Build ID: `3739c85b7628bc20cd6d5e7aea1bfe42a81a2792beddeb0e5e175c52760cea20`.
- Deploy result: success; Hosting version
  `projects/654072668208/sites/distillation-simulator/versions/e97991e487ddbb58`.
- HTTPS asset checks: `/`, `/app.js`, `/styles.css`, `/build-info.json` returned
  200; all bytes matched the source build. `/phase2-nonexistent` and `/api/health`
  returned 404, confirming the static-only boundary.
- Browser smoke: Firebase connection OK and expected build metadata visible;
  valid default submission preserves NOT CALCULATED/ENGINE NOT CONNECTED with
  the backend-unavailable warning; NF=11 with N=10 shows the expected error;
  reset restores NF=5 and clears the error; sensitivity tab is disabled for
  execution and switching back works; partial condenser is unavailable.
  Controls were tested via keyboard Enter because pointer automation was
  inconclusive. No scientific results are fabricated.

The 2026-09-25 project-access failure is historical and resolved for the
current authorized CLI session. No replacement project or configuration change
was necessary. This evidence completes the Phase 2 static demo DoD, not the
Phase 10 scientific production-release gate.
