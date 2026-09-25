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

Current working phase: **Phase 2 — FIREBASE EARLY CONNECTION**

Current status: **IN PROGRESS**

The repository has a tested backend/API skeleton and a dependency-free static
UI shell. It is not yet a working scientific simulator. The Firebase target is
configured in the repository, but the legacy project/site is inaccessible to
the current CLI session. This is a technical migration task, not an Owner
blocker: the student team may create/use a new Firebase project/site, update
the configuration, deploy and verify it.

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

Status: **IN PROGRESS**

Completed:

- Firebase target `distillation-simulator` is configured in the repository and
  PR #2 is merged to `main`.
- Target/site selection was recorded on 2026-09-24; re-verification on
  2026-09-25 returned HTTP 403 for the current CLI session.
- Static-only Hosting configuration and deterministic public build metadata added.
- Demo displays build/project information and preserves ENGINE NOT CONNECTED.
- Local structure, format, lint, mypy, 13 tests, frontend/package builds and
  secret scan pass. GitHub PR CI run `36154667511` passed for merge commit
  `bc4d2e5e07451c8d9d8c18e4f23f633fa3e99b52`. No credentials are stored in the
  repository.
- Production build from merge commit `bc4d2e5e07451c8d9d8c18e4f23f633fa3e99b52`
  produced build ID
  `3739c85b7628bc20cd6d5e7aea1bfe42a81a2792beddeb0e5e175c52760cea20`.

Remaining:

- Use an accessible student Firebase account/project/site, or create a new
  project/site; update `.firebaserc`/`firebase.json` to the selected target.
- Deploy Hosting, verify the public URL and record release/build evidence after
  a successful production smoke test.

Blockers: No scientific blocker. The legacy `distillation-simulator` target is
inaccessible (`firebase projects:list` omits it and its Hosting/deploy commands
returned HTTP 403), but the technical team is authorized to create or select a
student-controlled replacement. No production URL exists yet.

Next Action: Create/select a student-controlled Firebase project/site, update
the repository target, deploy the static build, then run HTTP/browser production
smoke tests.

Evidence: `firebase.json`, `.firebaserc`,
`tests/integration/test_frontend_build.py`; merge commit
`bc4d2e5e07451c8d9d8c18e4f23f633fa3e99b52`; CI run `36154667511`; CLI `15.19.0`;
build ID `3739c85b7628bc20cd6d5e7aea1bfe42a81a2792beddeb0e5e175c52760cea20`;
deploy attempted 2026-09-25 and failed with project-access error; production
URL: none. Autonomy policy updated 2026-09-25: create/select a replacement
student-controlled target rather than waiting for legacy-project access.

Last Updated: 2026-09-25

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

Blockers: All preceding phases and authorized deployment access.

Next Action: Start only after Phase 9 is DONE.

Evidence: `docs/ROADMAP.md`, `docs/DEPLOYMENT_RUNBOOK.md` and no production URL
currently recorded.

Last Updated: 2026-09-19

## Cross-phase blockers

- Reviewed Antoine dataset: blocks Phase 3/4 scientific output.
- Partial-condenser equations/reference case: `DEFERRED` and
  `BLOCKED` by scientific decision; keep the API `NOT_IMPLEMENTED`.
- Reviewed Cp/latent-heat data: blocks Phase 6 only.
- Phase 2 has no production URL or smoke-test PASS yet. The legacy Firebase
  target is inaccessible; create/select a student-controlled replacement and
  update the repository configuration before deploying.
- Separate backend runtime: required before production deployment; Firebase
  Hosting serves frontend/static assets only.
