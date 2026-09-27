# Handover

## Current Phase and Status

Phase 3 — MINIMUM CALCULATION ENGINE: `BLOCKED` by TODO-001 reviewed Antoine
records. Phase 0/1 are `DONE`; Phase 2 is `IN PROGRESS` until its evidence PR is merged;
Phase 4–10 are `NOT STARTED`.

## Completed checkpoint — 2026-09-27

- Existing Firebase project/site access reverified; no migration needed.
- Deployed main `f09b299200cfec94c85139a97c4a98d0cc2a946f` after green CI
  `36157068321` and local quality gates (13 tests; zero secret findings).
- Public static demo: https://distillation-simulator.web.app.
- Hosting version `e97991e487ddbb58`; build
  `3739c85b7628bc20cd6d5e7aea1bfe42a81a2792beddeb0e5e175c52760cea20`.
- HTTP asset-byte/404 checks and keyboard browser interaction smoke passed.
  Full evidence and redeploy steps are in `DEPLOYMENT_RUNBOOK.md`.
- No runtime, scientific data or configuration change was required.

## Remaining and scientific blockers

- TODO-001: scientific lead approves Antoine coefficients, units, applicable
  ranges, citations, reviewer and review date before Phase 3 scientific output.
- Implement minimum engine and total-condenser closure only against the
  approved contract; direct NF indexing, no geometric-stage rejection gate.
- Partial-condenser equations/reference case remain DEFERRED/BLOCKED; keep
  `NOT_IMPLEMENTED`. Reviewed enthalpy data blocks Phase 6 only.
- Functional UI, energy, sensitivity, validation and Phase 10 release remain
  unfinished. Firebase Hosting serves static files, not the Python API.

## Next action

Publish the local deployment-evidence checkpoint through PR CI/review and
merge; current GitHub integration cannot write (HTTP 403), and the browser
requires an authorized login. Then close Phase 2 and proceed to the scientific gate.

Read `PROJECT_RULES.md`, `ROADMAP.md`, `PROGRESS.md`, TODO-001 and
`THERMODYNAMIC_DATA_SPEC.md`. Obtain the scientific-lead decision on Antoine
records; do not invent data or record approval on the reviewer's behalf.
Technical work remains autonomous with CI/review; update PROGRESS at each
meaningful checkpoint. TASK DONE is not PHASE DONE.
