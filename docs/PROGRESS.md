# Progress

## Operating rule

**NO WORK IS COMPLETE UNTIL PROGRESS IS UPDATED.** Every meaningful checkpoint
follows `READ CURRENT STATE → IMPLEMENT → TEST → UPDATE DOCS → COMMIT/PUSH →
PR → CI/REVIEW → MERGE MAIN → BUILD PRODUCTION → DEPLOY FIREBASE HOSTING →
PRODUCTION SMOKE TEST → UPDATE EVIDENCE → CLOSE PHASE IF DoD PASSES → CONTINUE
NEXT PHASE`.
Task completion must not be reported as phase completion. The four allowed
phase statuses are `NOT STARTED`, `IN PROGRESS`, `BLOCKED` and `DONE`.

## Current project position

Current working phase: **Phase 4 — MCCABE–THIELE ENGINE**

Current status: **IN PROGRESS** (Phase 2 is merged and deployed; the reviewed
thermodynamic data and minimum total-condenser calculation path are now wired
locally, while UI integration and scientific reference validation remain).

Phase 2 Hosting uses the Firebase project owned by
`bichloannb06@gmail.com`: `delta-pagoda-509904-j8`. The repository has a tested
backend/API skeleton and a static UI shell, not an operational scientific
simulator. Phase 3 cannot produce scientific output until the scientific lead
approves the Antoine records.

## Phase status ledger

### Phase 0 — SPEC FREEZE

Status: **DONE**

Completed:

- V1 scope, input conventions, residual gates and architecture boundaries are
  recorded in the specification set.
- Open scientific/deployment items have owners or explicit blocking/deferred
  labels.
- Direct `NF` section switching, total-condenser closure direction and the
  partial-condenser boundary are documented.

Remaining:

- None for the Phase 0 Definition of Done. Open scientific items remain
  blockers for later phases and are listed below/TODO.

Blockers: None for Phase 0.

Next Action: Use the frozen contracts; do not invent unresolved scientific
data or equations.

Evidence: `afb7bfa` and the current contract/reference test suite.

Last Updated: 2026-09-19

### Phase 1 — PROJECT SKELETON

Status: **DONE**

Completed:

- Python API/engine skeleton, repository boundaries and local commands exist.
- Dependency-free UI shell exists in `web/` with three-column layout, tabs,
  input controls and explicit `ENGINE NOT CONNECTED`/`NOT CALCULATED` states.
- `scripts/build_frontend.py` builds the static shell and CI invokes it.
- Local backend health/thermo-version check and static frontend HTTP check pass.
- The complete local Phase 1 gate passes: structure, format, lint, mypy,
  frontend build, 11 unit/integration/reference/validation tests, package build
  and secret scan.
- GitHub Actions run `35499694516` is green at commit `86a0a1768ac50c926c83dd032ef7022c46e262ea`.

Remaining:

- None for the Phase 1 Definition of Done. Keep the skeleton/build/test
  contract green as later phases proceed.

Blockers: None for Phase 1.

Next Action: Continue the confirmed Phase 2 deployment workflow. Do not turn
the shell into a calculator without completing the scientific phases.

Evidence: `86a0a1768ac50c926c83dd032ef7022c46e262ea`; GitHub Actions run
`35499694516` passed install, structure, format, lint, mypy, frontend build,
tests, package build and secret scan. The same checks passed locally on
2026-09-21, including 11 tests.

Last Updated: 2026-09-21

### Phase 2 — FIREBASE EARLY CONNECTION

Status: **DONE**

Completed:

- Static Hosting configuration, deterministic build metadata and demo shell
  were merged through PR #2; the demo preserves ENGINE NOT CONNECTED.
- Created a Google Cloud/Firebase project owned by `bichloannb06@gmail.com` on
  2026-09-27: `delta-pagoda-509904-j8`. Firebase is enabled, the default
  Hosting site exists, and Google Analytics is disabled for the static demo.
  Repository deployment configuration now targets this project exclusively.
- Main source `f09b299200cfec94c85139a97c4a98d0cc2a946f` passed GitHub CI
  `36157068321`. The current deployment worktree passed structure, format,
  lint, mypy, 14 tests and a zero-finding secret scan on 2026-09-27.
- The account owner deployed the static bundle successfully to
  https://delta-pagoda-509904-j8.web.app on 2026-09-27.
- Production browser smoke confirmed the metadata fix: `Firebase connection OK ·
  Static Hosting only`, project `delta-pagoda-509904-j8`, and build ID
  `70f1fd3097ee0c74c9238c6db58eac3d444593485167086c957d54ca5e6181f7`.
  A valid submission shows the backend-unavailable warning without fabricating
  scientific output; NF=11 with N=10 is rejected; reset restores NF=5. Partial
  condenser and sensitivity execution remain unavailable as designed.

- Reverified production on 2026-10-04: all four assets match the local build;
  both required 404 routes pass; browser validation/reset/no-calculation gates
  pass; Firebase CLI can list the account-owned Hosting site.
- Repeated every local quality gate, including 14 tests, isolated package
  build and zero-finding secret scan; all passed.

Remaining: None for the Phase 2 Definition of Done.

Blockers: None for Phase 2.

Next Action: Keep the functional engine changes behind tests; do not broaden
the deployment scope before the calculation path is validated.

Evidence: `DEPLOYMENT_RUNBOOK.md`; deployed working tree based on
`f09b299200cfec94c85139a97c4a98d0cc2a946f`; build ID
`70f1fd3097ee0c74c9238c6db58eac3d444593485167086c957d54ca5e6181f7`;
production browser smoke PASS. The sandbox denied terminal HTTP socket access,
so byte-for-byte asset and 404 checks were not repeated on 2026-09-27.
Those checks passed on 2026-10-04; see `docs/evidence/phase2-2026-10-04.json`.
This checkpoint still requires PR CI/review before Phase 2 is marked DONE.

Last Updated: 2026-10-04

### Phase 3 — MINIMUM CALCULATION ENGINE

Status: **DONE**

Completed:

- API schemas, Raoult–Antoine contracts, residual gates and calculation
  closure requirements are documented.
- NIST SRD 69 Ethanol–Water records were approved by GVHD on 2026-10-04 and
  committed with provenance in `data/thermodynamics/antoine_ethanol_water.json`.
- Bubble-point, Raoult equilibrium and controlled extrapolation warnings are
  implemented and covered by the existing contract tests.
- Ethanol record selection is deterministic: Record 1 is preferred in the
  approved overlap and Record 2 is used above Record 1 when in range.
- Total-mass and ethanol-balance outputs, recovery and outer residual metadata
  are returned by the minimum API calculation path.
- The total-condenser path rejects non-converged cases instead of clamping
  off-curve McCabe--Thiele steps into a fabricated result.
- The implementation boundary remains explicit; no fake result is exposed.
- Local smoke on 2026-10-04 confirmed the reviewed data path can run from
  input through xD/xB/recovery and controlled thermodynamic warning details.

Remaining:

- Add dedicated numerical reference cases against GVHD-approved examples.

Blockers: No data blocker remains. Scientific reference validation is still
required before claiming the engine is validated.

Next Action: Validate the total-condenser closure against approved reference
cases, then keep improving the UI path without adding new scientific models.

Evidence: `docs/THERMODYNAMIC_DATA_SPEC.md`, `docs/CALCULATION_FORMULAS.md`,
current pending-data tests, the API skeleton and
`docs/evidence/phase3-4-local-2026-10-04.json`.

Last Updated: 2026-10-04

### Phase 4 — MCCABE–THIELE ENGINE

Status: **IN PROGRESS**

Completed:

- Required direct `NF` section-switch convention and calculation closure gate
  are specified.
- Minimum total-condenser stepping and stage records are wired to the API.
- Rectifying line, q-line including `q=1`, stripping line and feed
  intersection are returned for graph rendering.
- The UI renders backend-calculated xD/xB/recovery, stage table and a
  McCabe--Thiele SVG plot from API data.
- Local smoke on 2026-10-04 rendered the end-to-end total-condenser flow at
  `http://127.0.0.1:8000/`: input -> xD/xB/recovery/D/B -> stage data ->
  McCabe--Thiele plot -> detailed `THERMO_EXTRAPOLATION` warning.
- A golden-case request/template now exists so GVHD data can be mapped without
  inventing validation values.

Remaining:

- Add GVHD-approved golden/reference cases for stage profile and plot geometry.

Blockers: Reference validation.

Next Action: Validate total-condenser stage profile against an approved
reference case; keep partial condenser `NOT_IMPLEMENTED`.

Evidence: `docs/ROADMAP.md`, `docs/ALGORITHM_SPEC.md`,
`docs/TEST_CASES.md` and
`docs/evidence/phase3-4-local-2026-10-04.json`;
`docs/VALIDATION_REQUEST.md`.

Last Updated: 2026-10-04

### Phase 5 — MINIMUM FUNCTIONAL UI

Status: **IN PROGRESS**

Completed:

- Static presentation shell exists.
- Local UI now submits to the local API and renders backend-calculated
  xD/xB/recovery/D/B, stage table, McCabe--Thiele plot and warning details.
- UI form on `main` was restyled toward the supervisor-provided layout while
  preserving the existing backend/API calculation path.

Remaining:

- Add approved reference validation evidence before calling the UI scientifically
  validated.
- Production deployment still needs a backend runtime decision; Firebase Hosting
  alone remains static.

Blockers: Scientific reference validation and later backend runtime decision.

Next Action: Keep the local functional UI path stable while reference cases are
reviewed; do not add sensitivity or new scientific models yet.

Evidence: `web/` shell build in `afb7bfa`,
`docs/evidence/phase3-4-local-2026-10-04.json` and local frontend/API tests.

Last Updated: 2026-10-06

### Phase 6 — ENERGY

Status: **NOT STARTED**

Completed: None.

Remaining: Review Cp/latent-heat sources and implement/test `calcEnergy` with
the approved reference and sign convention.

Blockers: Reviewed enthalpy data and Phase 4/5 result contracts.

Next Action: Review energy data only after the earlier calculation path is
stable.

Evidence: Energy contract is documented; no production energy implementation.

Last Updated: 2026-09-19

### Phase 7 — SENSITIVITY

Status: **NOT STARTED**

Completed: Sensitivity boundary for changing exactly one of `R`, `N` or `NF`
is documented.

Remaining: Implement sweeps, preserve all other inputs and test outputs.

Blockers: Validated calculation engine and API/UI integration.

Next Action: Start after the base simulation path is complete.

Evidence: Sensitivity schemas/contracts and pending tests.

Last Updated: 2026-09-19

### Phase 8 — SCIENTIFIC VALIDATION

Status: **NOT STARTED**

Completed: MAE metric and threshold are recorded in
`VALIDATION_ACCEPTANCE.md`.

Remaining: Review source/mapping, run reference cases and record results.

Blockers: Reviewed validation source and a completed calculation engine.

Next Action: Prepare validation only after scientific output is available.

Evidence: `docs/VALIDATION_ACCEPTANCE.md` and validation test scaffolding.

Last Updated: 2026-09-19

### Phase 9 — PRODUCT HARDENING

Status: **NOT STARTED**

Completed: CI baseline and security-scan command exist.

Remaining: Harden CI/release flow, document backend runtime and complete
staging/iterative deployment checks.

Blockers: Earlier phases, deployment target and backend runtime decision.

Next Action: Start after functional validation.

Evidence: `.github/workflows/ci.yml` and current local checks.

Last Updated: 2026-09-19

### Phase 10 — PRODUCTION RELEASE

Status: **NOT STARTED**

Completed: Production acceptance criteria are documented.

Remaining: Final build/deploy, backend runtime, production smoke test and
recorded URL/release evidence.

Blockers: All preceding phases and authorized deployment access.

Next Action: Start only after Phase 9 is DONE.

Evidence: `docs/ROADMAP.md` and `docs/DEPLOYMENT_RUNBOOK.md`; the Phase 2 static
demo URL exists, but the full Phase 10 production release is not complete.

Last Updated: 2026-09-19

## Cross-phase blockers

- Reviewed Antoine dataset: resolved for Ethanol-Water Phase 3/4 runtime use.
- Reviewed reference/golden validation case: blocks claiming scientific
  validation PASS.
- Partial-condenser equations/reference case: `DEFERRED` and
  `BLOCKED` by scientific decision; keep the API `NOT_IMPLEMENTED`.
- Reviewed Cp/latent-heat data: blocks Phase 6 only.
- Phase 2 deployment and static smoke checks passed; no current Hosting blocker.
- Separate backend runtime: required before production deployment; Firebase
  Hosting serves frontend/static assets only.
