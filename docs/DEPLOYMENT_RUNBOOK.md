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

Current target/site: `delta-pagoda-509904-j8`, created under
`bichloannb06@gmail.com` on 2026-09-27. Firebase is enabled and the default
Hosting site exists. Use this target for every future Firebase Hosting phase;
do not rely on another person's Firebase project. Google Analytics is disabled
for the static demo. Keep credentials outside the repository.

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

## Previous Phase 2 evidence — 2026-09-27

- Verified: 2026-09-27.
- Source baseline: `f09b299200cfec94c85139a97c4a98d0cc2a946f` (main, PR #5
  merge); the deployed metadata fix is awaiting its evidence PR.
- CI: https://github.com/Quangbk47/distillation-simulator/actions/runs/36157068321
  â€” completed, success.
- Local gate: structure, format, lint, mypy and 14 tests passed; detect-secrets
  reported zero findings. TestClient emitted one upstream deprecation warning;
  no failures. A package build could not be repeated because the sandbox blocks
  outbound setup access and the local virtual environment lacks setuptools.
- Project/site: `delta-pagoda-509904-j8` (account-owned default Hosting site).
- URL: https://delta-pagoda-509904-j8.web.app.
- Build ID: `70f1fd3097ee0c74c9238c6db58eac3d444593485167086c957d54ca5e6181f7`.
- Deploy result: success, confirmed by the account owner on 2026-09-27.
- Browser smoke: Firebase connection OK with project
  `delta-pagoda-509904-j8` and expected build metadata visible;
  valid default submission preserves NOT CALCULATED/ENGINE NOT CONNECTED with
  the backend-unavailable warning; NF=11 with N=10 shows the expected error;
  reset restores NF=5 and clears the error; sensitivity tab is disabled for
  execution and switching back works; partial condenser is unavailable.
  Controls were tested via keyboard Enter because pointer automation was
  inconclusive. No scientific results are fabricated. The sandbox denied the
  terminal's post-deploy HTTP socket test, so asset-byte and 404 checks were
  not repeated for this deployment.

The former project access issue is historical. This account-owned deployment
passes the Phase 2 production and browser-smoke gates; its evidence still needs
the required commit, PR CI/review and merge. It is not the Phase 10 scientific
production-release gate.

## Latest Phase 2 verification — 2026-10-04

The recorded 2026-09-25 HTTP 403 concerned the former project
`distillation-simulator` and occurred before upload. The surviving record
establishes a project-access failure, not the exact denied IAM permission.
Do not diagnose it as a frontend defect or change permissions on that project.
The documented account-owned replacement `delta-pagoda-509904-j8` is accessible:
`firebase hosting:sites:list --project delta-pagoda-509904-j8 --non-interactive`
succeeded and returned https://delta-pagoda-509904-j8.web.app.

- Source: `0a739bded5b59ec352b1f026e1efdfc5a9355a49`, local evidence branch.
  Fetch succeeded; remote main remains `f09b299200cfec94c85139a97c4a98d0cc2a946f`.
- Existing production deployment reverified; no deployment was performed in
  this session. All four public assets match the locally rebuilt artifact
  byte-for-byte. Unknown path and `/api/health` both return HTTP 404.
- Browser smoke: expected project/build and static Hosting status; valid
  submission leaves results NOT CALCULATED with the backend-unavailable
  warning; NF=11/N=10 rejected; reset restores NF=5 and clears the error;
  sensitivity execution and partial condenser remain disabled.
- Structure, formatting, lint, mypy, frontend build, 14 tests, isolated package
  build (sdist/wheel), and zero-finding secret scan all pass. One upstream
  TestClient deprecation warning remains. The previous network/package-build
  verification limitations are resolved for this session.
- Machine-readable HTTP hashes and check results:
  [phase2-2026-10-04.json](evidence/phase2-2026-10-04.json).
- Publication remains unfinished: noninteractive GitHub push dry-run exits
  128 and the available GitHub browser is signed out. A write-authorized
  account session is required; no Firebase account action is currently needed.
- Next: publish the existing evidence branch, open PR, require green CI and
  review, merge, then build/deploy the merged green source and repeat smoke
  checks. Keep Phase 2 IN PROGRESS until that sequence and evidence are complete.

Scientific gates remain unchanged: TODO-001 reviewed ethanol/water Antoine
records block Phase 3/4 output; partial condenser remains NOT_IMPLEMENTED;
reviewed enthalpy data blocks Phase 6 only. This is a static demo, not the
Phase 10 scientific production release.
