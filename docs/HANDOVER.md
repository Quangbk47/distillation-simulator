# Handover

## Current Phase and Status

Phase 3 — MINIMUM CALCULATION ENGINE: `BLOCKED` by TODO-001 reviewed Antoine
records. Phase 0/1 are `DONE`; Phase 2 is `IN PROGRESS` until its evidence PR is merged;
Phase 4–10 are `NOT STARTED`.

## Completed checkpoint — 2026-09-27

- Firebase project/site `delta-pagoda-509904-j8` was created under
  `bichloannb06@gmail.com`; all future Hosting work uses this target.
- Production static demo deployed successfully: https://delta-pagoda-509904-j8.web.app.
  The deployment build is
  `70f1fd3097ee0c74c9238c6db58eac3d444593485167086c957d54ca5e6181f7`.
- Browser smoke confirmed `Firebase connection OK · Static Hosting only` and
  project `delta-pagoda-509904-j8`; valid submit keeps scientific output absent,
  invalid NF is rejected, and reset restores NF=5. The worktree passed 14 tests
  and a zero-finding secret scan. Full evidence is in `DEPLOYMENT_RUNBOOK.md`.
- The terminal sandbox denied HTTP socket access, so post-deploy byte/404 checks
  were not repeated; the direct browser smoke passed.

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

Commit and publish the local deployment-evidence checkpoint through PR
CI/review and merge. Then obtain the scientific-lead data approval before
starting Phase 3.

Read `PROJECT_RULES.md`, `ROADMAP.md`, `PROGRESS.md`, TODO-001 and
`THERMODYNAMIC_DATA_SPEC.md`. Obtain the scientific-lead decision on Antoine
records; do not invent data or record approval on the reviewer's behalf.
Technical work remains autonomous with CI/review; update PROGRESS at each
meaningful checkpoint. TASK DONE is not PHASE DONE.
