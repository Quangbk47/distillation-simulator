# Handover

## Current Phase and Status

Phase 2 is `DONE`. Phase 3 is `DONE` for the reviewed Ethanol-Water
Raoult-Antoine minimum engine. Phase 4/5 are `IN PROGRESS` for total-condenser
McCabe-Thiele and the local functional UI. Phase 6/7/8/9/10 remain gated by
their documented dependencies.

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

- TODO-001 is resolved: GVHD approved the Ethanol-Water NIST SRD 69 Antoine
  records on 2026-10-04, and the reviewed runtime dataset is committed.
- Continue total-condenser closure only against the approved contract; direct
  NF indexing, no geometric-stage rejection gate.
- A GVHD-approved golden/reference case is still needed before claiming
  scientific validation PASS. The supervisor-form candidate is recorded but
  currently conflicts with material balance, so it is not a pass case.
- Partial-condenser equations/reference case remain DEFERRED/BLOCKED; keep
  `NOT_IMPLEMENTED`. Reviewed enthalpy data blocks Phase 6 only.
- Functional UI, energy, sensitivity, validation and Phase 10 release remain
  unfinished. Firebase Hosting serves static files, not the Python API.

## Next action

Read `PROJECT_RULES.md`, `ROADMAP.md`, `PROGRESS.md`, `TODO.md` and the
validation files before continuing. Keep improving the local Phase 4/5 path
without inventing validation data, partial-condenser equations or energy
constants. Ask GVHD for the authoritative reference case before promoting
scientific validation. Technical work remains autonomous with CI/review; update
PROGRESS at each meaningful checkpoint. TASK DONE is not PHASE DONE.
