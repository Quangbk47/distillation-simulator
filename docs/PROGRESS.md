# Progress

## Operating rule

**NO WORK IS COMPLETE UNTIL PROGRESS IS UPDATED.** Every meaningful checkpoint
follows `IMPLEMENT → TEST → UPDATE PROJECT DOCUMENTATION → COMMIT → PUSH`.
Task completion must not be reported as phase completion. The four allowed
phase statuses are `NOT STARTED`, `IN PROGRESS`, `BLOCKED` and `DONE`.

## Current project position

Current working phase: **Phase 2 — FIREBASE EARLY CONNECTION**

Current status: **BLOCKED**

The repository has a tested backend/API skeleton and a dependency-free static
UI shell. It is not yet a working scientific simulator. Phase 2 cannot proceed
past planning until the owner confirms the Firebase account and target project.

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

Next Action: Confirm the Firebase account and target project for Phase 2. Do
not turn the shell into a calculator without completing the scientific phases.

Evidence: `86a0a1768ac50c926c83dd032ef7022c46e262ea`; GitHub Actions run
`35499694516` passed install, structure, format, lint, mypy, frontend build,
tests, package build and secret scan. The same checks passed locally on
2026-09-21, including 11 tests.

Last Updated: 2026-09-21

### Phase 2 — FIREBASE EARLY CONNECTION

Status: **BLOCKED**

Completed:

- Frontend hosting scope and the owner-confirmation requirement are documented.
- No project, credentials or deployment configuration has been guessed or
  created.

Remaining:

- Owner confirms Firebase account/login and target project ID.
- Add minimal Hosting configuration, deploy the static shell and record URL.
- Run hosting smoke test and record the deployment evidence.

Blockers: Owner Firebase login/project selection and a confirmed target.

Next Action: Ask the repository owner to log in/select the intended Firebase
project; stop at that external action.

Evidence: Repository inventory shows no `firebase.json` or `.firebaserc`;
local frontend build is PASS; no Firebase URL exists.

Last Updated: 2026-09-19

### Phase 3 — MINIMUM CALCULATION ENGINE

Status: **BLOCKED**

Completed:

- API schemas, Raoult–Antoine contracts, residual gates and calculation
  closure requirements are documented.
- The implementation boundary remains explicit; no fake result is exposed.

Remaining:

- Review and approve Antoine component records, units, ranges, citation,
  reviewer and date.
- Implement/test VLE, bubble temperature, balances, recovery and residual
  gates, followed by the total-condenser outer solve and reboiler boundary.

Blockers: Reviewed Antoine data is required for scientific output.

Next Action: Scientific lead reviews the Antoine records; then implement only
against the approved data contract.

Evidence: `docs/THERMODYNAMIC_DATA_SPEC.md`, `docs/CALCULATION_FORMULAS.md`,
current pending-data tests and the API skeleton.

Last Updated: 2026-09-19

### Phase 4 — MCCABE–THIELE ENGINE

Status: **NOT STARTED**

Completed:

- Required direct `NF` section-switch convention and calculation closure gate
  are specified.

Remaining:

- Complete Phase 3 first, then implement stepping, operating lines, stage
  count, feed split and total-condenser path with reference tests.

Blockers: Phase 3 output/data and the calculation closure gate.

Next Action: Start only after Phase 3 and closure-gate evidence are complete.

Evidence: `docs/ROADMAP.md`, `docs/ALGORITHM_SPEC.md` and `docs/TEST_CASES.md`.

Last Updated: 2026-09-19

### Phase 5 — MINIMUM FUNCTIONAL UI

Status: **NOT STARTED**

Completed:

- Static presentation shell only; it deliberately does not calculate.

Remaining:

- Connect the UI to the validated API, render real results/warnings/stages and
  add the required manual/API smoke evidence.

Blockers: Phase 4 engine and API contract completion.

Next Action: Begin after Phase 4 is DONE.

Evidence: `web/` shell build in `afb7bfa`; no engine connection exists.

Last Updated: 2026-09-19

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

Blockers: All preceding phases and owner-managed deployment access.

Next Action: Start only after Phase 9 is DONE.

Evidence: `docs/ROADMAP.md`, `docs/DEPLOYMENT_RUNBOOK.md` and no production URL
currently recorded.

Last Updated: 2026-09-19

## Cross-phase blockers

- Reviewed Antoine dataset: blocks Phase 3/4 scientific output.
- Partial-condenser equations/reference case: `DEFERRED` and
  `BLOCKED` by scientific decision; keep the API `NOT_IMPLEMENTED`.
- Reviewed Cp/latent-heat data: blocks Phase 6 only.
- Firebase account/project confirmation: blocks Phase 2 deployment work.
- Separate backend runtime: required before production deployment; Firebase
  Hosting serves frontend/static assets only.
