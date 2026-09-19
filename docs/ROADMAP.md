# Roadmap — V1 implementation and release

## How to use this roadmap

This is the execution contract for a student team. Work top-to-bottom, keep
the engine independent from the UI, and do not mark a phase complete from a
document-only claim. Every phase has an objective, tasks, deliverables, tests,
definition of done, dependencies and blockers.

Phase status and evidence are maintained in `PROGRESS.md`; unresolved work is
maintained in `TODO.md`. This roadmap is not a task diary. Follow the mandatory
workflow in `PROJECT_RULES.md`: **NO WORK IS COMPLETE UNTIL PROGRESS IS
UPDATED.**

The authoritative scope is Ethanol–Water, steady-state, binary, constant
pressure, Raoult + Antoine, McCabe–Thiele, simple energy, and sensitivity of
exactly one of `R`, `N` or `NF`. System 2, Wilson/NRTL, optimization, dynamic
simulation, detailed tray hydraulics, microservices and Kubernetes are
deferred.

Important implementation order: Firebase Hosting is connected early to prove
the frontend delivery path, then used again for iterative and final releases.
Firebase Hosting serves frontend/static assets only; the Python backend/API
must run on a separate suitable runtime.

## Phase 0 — SPEC FREEZE

**Objective**

Freeze the V1 scope and calculation contract before scientific code is written.

**Inputs**

Existing final docs, current schemas/source/tests, signed decisions and the
independent audit.

**Files/modules expected to change**

`docs/*.md`, `src/api/schemas.py` only when a documented contract mismatch is
found, and contract tests.

**Owner/role**

Scientific lead + project owner; student developer records the result.

**Tasks**

- Read `PROJECT_SCOPE.md`, `PROJECT_RULES.md`, `EXPERT_CONFIRMATION.md`,
  `EXPERT_DECISIONS.md`, `PROCESS_MODEL.md`, `ALGORITHM_SPEC.md`,
  `CALCULATION_FORMULAS.md`, `DATA_MODEL.md`, `THERMODYNAMIC_DATA_SPEC.md`,
  `UI_UX_SPEC.md`, `TEST_CASES.md`, `VALIDATION_*` and this roadmap.
- Record CHỐT, OPEN, BLOCKING and DEFERRED decisions in the issue/PR.
- Resolve any scientific conflict through the source-of-truth hierarchy in
  `docs/PROJECT_AUDIT.md`; never resolve it silently in code.

**Deliverables**

- Reviewed scope/spec set and a signed decision for any newly blocking item.
- Input/output field list with units and status/error conventions.

**Tests**

- Documentation consistency review against `PROJECT_AUDIT.md`.
- Contract tests for direct `q`, absolute `heatLoss_kW`, `N/NF`, condenser
  modes and residual gate.

**Definition of Done**

Student can start implementation without inventing a scientific model; every
OPEN item has an owner and a blocking/deferred label.

**What NOT to do**

Do not select Antoine/enthalpy coefficients, partial-condenser equations or a
Firebase project by guesswork. Do not start the main engine before closure.

**Dependencies**

Existing final documents and the calculation specification.

**Blockers**

Reviewed Antoine data remains blocking for Phase 3/4 scientific output; reviewed
enthalpy data blocks only Phase 6 energy. The Firebase project/account target
remains blocking for deployment.

## Phase 1 — PROJECT SKELETON

**Objective**

Clone, install, test and run a minimal app locally.

**Inputs**

Phase 0 contract, `pyproject.toml`, existing `src/`, tests and CI workflow.

**Files/modules expected to change**

`src/ui/`, minimal static frontend files, `README.md`, `pyproject.toml` only if
needed, and `.github/workflows/ci.yml`.

**Owner/role**

Student developer; reviewer checks CI.

**Tasks**

- Keep the `src/` module boundaries and add only the minimum frontend/static
  app needed for a health/status screen.
- Install dependencies from `pyproject.toml`; keep `.env` local and secret-free.
- Keep CI steps: install → structure → format → lint → type-check → tests →
  build → secret scan.
- Decide and document the backend local command and frontend build command.

**Deliverables**

- Minimal local app with a visible project/version/health status.
- Passing CI workflow on a pull request.

**Tests**

- Structure, format, lint, mypy, current unit/integration/reference tests and
  package/frontend build.

**Definition of Done**

Fresh clone runs locally using documented commands; CI is green; no secret,
thermo coefficient or fake simulation result is committed.

**What NOT to do**

Do not implement scientific placeholder values, add a frontend calculation
copy, or introduce a framework/backend runtime without documenting it.

**Dependencies**

Phase 0.

**Blockers**

Missing toolchain or an undocumented frontend choice.

## Phase 2 — FIREBASE EARLY CONNECTION

**Objective**

Prove the minimum frontend delivery path early, before the calculation engine
is complete.

**Inputs**

Phase 1 status UI, `UI_UX_SPEC.md`, owner-confirmed Firebase target/account and
deployment runbook.

**Files/modules expected to change**

Frontend shell, `firebase.json`, `.firebaserc` or documented equivalent,
hosting workflow/config and deployment record.

**Owner/role**

DevOps/deployment owner with repository owner for login/project confirmation.

**Tasks**

- Inventory `firebase.json`, `.firebaserc`, hosting config, workflow and
  environment variables. At audit time none exists.
- Confirm the target Firebase project and account with the owner. Do not create
  a project, guess a project ID, or handle credentials automatically.
- If login is required, stop at the login step and ask the owner to complete
  it. Never commit tokens, passwords, service-account keys or API secrets.
- Add minimal hosting configuration and a static status page showing project,
  build/commit and `Firebase connection OK` only after the target is known.
- Use manual deploy first if automatic deploy is not yet appropriate.

**Deliverables**

- `firebase.json` and `.firebaserc` (or documented owner-managed equivalent).
- Public test/staging URL, or a recorded blocker if login/project confirmation
  is pending.
- A short deployment record with project ID and commit, without secrets.

**Tests**

- Local frontend build.
- Hosting preview/deploy smoke test for the static page.
- Confirm no Python API is being presented as Firebase Hosting execution.

**Definition of Done**

The minimum UI is reachable at a Firebase URL and can be redeployed from a
known commit; CI remains a prerequisite for any automated deploy.

**What NOT to do**

Do not create/guess a Firebase project, commit credentials, deploy fake
scientific numbers, or claim Firebase Hosting runs the Python API.

**Dependencies**

Phase 1 and owner confirmation of Firebase target/account.

**Blockers**

Firebase login, project ID, billing/permissions, or hosting target not yet
confirmed. This phase must stop at that boundary rather than inventing setup.

## Parallel work after Phase 2

These tracks may proceed in parallel after the UI shell is reachable:

- scientific lead reviews the Antoine dataset for Phase 3/4;
- backend team implements/tests the total-condenser calculation closure and
  direct NF section-switch contract;
- scientific lead answers the partial-condenser OPEN/BLOCKING questions and
  supplies a reviewed reference case;
- frontend team keeps the Firebase UI shell labeled `DEMO`, `NOT CALCULATED`
  and `ENGINE NOT CONNECTED` until a real API result exists.

Enthalpy/Cp review is intentionally a Phase 6 track and does not block the
Phase 3/4 VLE and stage implementation.

## Phase 3 — MINIMUM CALCULATION ENGINE

**Objective**

Produce a deterministic, testable material/VLE foundation without UI coupling.

**Inputs**

Phase 0 contract, reviewed Antoine dataset, `PROCESS_MODEL.md` and VLE test
fixtures/reference sources.

**Files/modules expected to change**

`src/thermodynamics/`, material-balance/solver modules under
`src/distillation/`/`src/solver/`, reviewed data files, unit/reference tests.

**Owner/role**

Backend student developer with scientific reviewer for data.

**Tasks**

- Load only reviewed Antoine records with provenance and version.
- Implement Antoine, Raoult VLE, bubble temperature/equilibrium inversion,
  material balance, ethanol balance and ethanol recovery.
- Implement physical input checks, normalized residuals and structured
  extrapolation warnings.
- Keep pending data clearly unavailable; do not substitute unreviewed values.

**Deliverables**

- Pure thermo/material-balance modules and typed result fragments.
- Reviewed data file or an explicit blocked status.

**Tests**

- Antoine in-range, extrapolated and nonphysical cases.
- Bubble point at pure-component limits and representative composition.
- Total/component balance, recovery formula and residual gate.

**Definition of Done**

All Phase 3 functions are deterministic and independently tested; no result is
reported as success without reviewed data and the mass/component/outer/solver
residual gates defined by the calculation contract.

**What NOT to do**

Do not implement energy, partial-condenser assumptions or UI calculations here;
do not hard-code unreviewed Antoine coefficients.

**Dependencies**

Phase 0–1 and reviewed Antoine data.

**Blockers**

No approved coefficients, units, range, citation, reviewer and review date.

## Calculation Closure Gate — required before Phase 4

Phase 4 cannot start until a reviewer accepts the total-condenser formulation
in `PROCESS_MODEL.md` and its tests cover:

- scalar unknown `xD` and derived `xB`;
- physical xD bounds and deterministic bracket/search interval;
- outer residual `y_N - y_eq(xB,P)` and numerical method;
- top total-condenser boundary, body-stage indexing and equilibrium reboiler
  boundary;
- `NF` transition uses the direct input index; q-line intersection is
  diagnostic geometry, not an additional success gate;
- no-bracket, pinch, out-of-range and non-convergence behavior.

The gate is not satisfied by a document-only placeholder or by a test that
uses invented thermo values. It is satisfied when the contract and analytic
tests are reviewed and the engine implementation can be written directly.

## Phase 4 — MCCABE–THIELE ENGINE

**Objective**

Implement the stage solver and explicit condenser branches.

**Inputs**

Phase 3 VLE/balance functions, the calculation-closure gate, approved NF
convention and (for partial) an approved scientific contract.

**Files/modules expected to change**

`src/distillation/mccabe_thiele.py`, operating-line/stage modules,
`src/solver/`, condenser tests and reference tests.

**Owner/role**

Backend student developer; scientific lead approves partial formulation.

**Tasks**

- Implement diagonal, rectifying line, q-line including a no-division q=1
  branch, stripping line and feed intersection.
- Implement stepping, `NF`, body-stage `N`, stage compositions and bubble
  temperatures.
- Implement total condenser first; implement partial condenser as its own
  equilibrium-stage branch, not a renamed total branch.
- Return `non_converged`/physical errors with trace rather than fake numbers.

**Deliverables**

- McCabe–Thiele engine with both condenser modes and typed stage table.

**Tests**

- q=1, q≠1, operating-line intersections, pinch/out-of-range cases,
  `N/NF`, total/partial condenser reference cases and stage temperature.

**Definition of Done**

Both modes have independent tests; `N` excludes condenser/reboiler; all
stages are finite/physical; residual and solver gates are enforced.

**What NOT to do**

Do not begin before the Calculation Closure Gate, silently adjust NF, count
the reboiler/condenser in N, or enable partial with an invented equation. Do
not add a geometric-stage rejection mechanism to V1.

**Dependencies**

Phase 3 and the explicit partial-condenser reference contract.

**Blockers**

Partial-condenser equilibrium convention or reference case not approved.

## Phase 5 — MINIMUM FUNCTIONAL UI

**Objective**

Make the complete basic user flow usable: input → Run Simulation → output.

**Inputs**

Stable typed API result, `UI_UX_SPEC.md`, process visualization requirements
and the early Firebase shell.

**Files/modules expected to change**

`src/ui/`, frontend build/config, API integration tests and hosting deployment
record.

**Owner/role**

Frontend student developer with backend reviewer.

**Tasks**

- LEFT: input fields for approved variables, direct `q`, absolute heat loss and
  condenser mode.
- CENTER: simple column diagram and McCabe–Thiele plot.
- RIGHT: key results, warnings, residuals, stage table and basic graph.
- Keep all scientific calculations in the backend; frontend only renders typed
  output and displays persistent extrapolation warnings.
- Deploy this vertical slice to Firebase Hosting after CI passes.

**Deliverables**

- Functional browser UI and API integration for total/partial or explicit
  unavailable status.
- Iterative Firebase URL/version record.

**Tests**

- API schema/error tests, UI smoke test, normal case, invalid input, warning,
  non-converged case and output rendering.

**Definition of Done**

A student can enter a valid case, run it, and see numbers, diagram, stage
table, graph, warnings and residuals at a deployed URL without frontend
recalculation.

**What NOT to do**

Do not add tray efficiency/Tfeed/reboiler controls, fake demo values, 3D
animation, or duplicated calculation logic in the browser.

**Dependencies**

Phases 2–4.

**Blockers**

No stable API result contract or no Firebase target/config.

## Phase 6 — ENERGY

**Objective**

Add the simple, auditable QC/QR model without changing the core VLE scope.

**Inputs**

Phase 5 solution/stage output and reviewed Cp/latent-heat data with provenance.

**Files/modules expected to change**

`src/distillation/energy.py`, enthalpy data/schema, energy unit tests and API
result serialization.

**Owner/role**

Backend student developer with scientific reviewer.

**Tasks**

- Review Cp, latent heat, `Tref`, units and provenance.
- Implement pure `calcEnergy(input, solution, enthalpyData)`.
- Freeze sign convention: `QC < 0`, `QR > 0`, `heatLoss_kW >= 0` and loss
  increases required `QR` according to the formula contract.

**Deliverables**

- Energy breakdown with QC, QR and heat loss in kW.

**Tests**

- Fixture-based Cp/latent heat tests, unit conversion, sign convention and
  heat-loss delta tests.

**Definition of Done**

Energy outputs are reproducible, sourced, unit-tested and exposed only from
the engine/API.

**What NOT to do**

Do not block Phase 3/4 on enthalpy, invent constants, change QC/QR signs, or
infer q from Tfeed.

**Dependencies**

Phase 3–4 and reviewed enthalpy data.

**Blockers**

No approved Cp/latent heat data or unresolved sign convention.

## Phase 7 — SENSITIVITY

**Objective**

Provide simple R/N/NF sweeps with one changed variable at a time.

**Inputs**

Stable simulation API and the base-case input/result contract.

**Files/modules expected to change**

`src/sensitivity/runner.py`, API sensitivity schema/handler, UI sensitivity tab
and sensitivity tests.

**Owner/role**

Backend/frontend pair; reviewer checks invariant preservation.

**Tasks**

- Validate sweep values and preserve all non-target inputs, including q,
  condenser and heat loss.
- Return a typed series for key outputs and a simple chart.

**Deliverables**

- API/UI sensitivity screen or panel for R, N and NF.

**Tests**

- One-variable invariant tests, integer/range checks and failed-case handling.

**Definition of Done**

Each supported sweep changes exactly one variable and produces traceable,
chartable results; no optimizer is introduced.

**What NOT to do**

Do not sweep multiple variables, optimize a result, or change q/condenser/heat
loss implicitly.

**Dependencies**

Phase 5–6.

**Blockers**

Unstable base simulation or missing output series contract.

## Phase 8 — SCIENTIFIC VALIDATION

**Objective**

Evaluate reviewed reference cases without claiming validation prematurely.

**Inputs**

Stable engine, reviewed thermo/enthalpy data as applicable, literature or
experimental source and mapping review.

**Files/modules expected to change**

`data/validation/`, validation scripts/tests, `VALIDATION_PLAN.md` and review
report.

**Owner/role**

Scientific lead/reviewer; student prepares reproducible runs.

**Tasks**

- Review Antoine/Cp/latent heat citations, ranges, units, reviewer and date.
- Add literature/experimental cases with complete mapping and observed data.
- Run the accepted metric `MAE_xD_xB_percentage_points` with threshold `5`.
- Keep case status `READY_FOR_EVALUATION` until source and mapping review is
  complete; record PASS/FAIL evidence after evaluation.

**Deliverables**

- Golden/reference cases, reproducible validation report and review record.

**Tests**

- Schema/provenance checks, golden regression, metric calculation and
  threshold boundary tests.

**Definition of Done**

At least one reviewed case is reproducibly evaluated; validation status is
evidence-backed and never inferred from the configured threshold alone.

**What NOT to do**

Do not use the UI mockup as evidence, mark pending data PASS, or change the
accepted metric/threshold without a new decision.

**Dependencies**

Phases 3–7 and scientific reviewer.

**Blockers**

Missing source citation, condition mapping, observed values or reviewer.

## Phase 9 — PRODUCT HARDENING

**Objective**

Make normal, invalid and failure paths safe and understandable.

**Inputs**

All prior outputs, release checklist, selected backend runtime and staging
Firebase deployment.

**Files/modules expected to change**

API error/auth/configuration, frontend error states, CI/workflow, tests and
deployment documentation.

**Owner/role**

Release/DevOps owner with backend/frontend reviewers.

**Tasks**

- Harden input validation, warnings, non-convergence and extrapolation.
- Check responsive UI, error handling, API authorization/CORS, environment
  configuration and secret handling.
- Add structure, unit, integration, reference, validation, build and smoke
  coverage; protect main branch.
- Run iterative Firebase deploy only after CI passes.

**Deliverables**

- Release checklist, CI evidence, security/secret-scan evidence and staging
  deployment record.

**Tests**

- Normal, invalid, q=1, total/partial, extrapolation, energy, sensitivity,
  non-converged and unauthorized API cases.

**Definition of Done**

All known failure modes return typed errors/warnings; CI is green; staging
smoke tests pass; no secret or unreviewed scientific data is shipped.

**What NOT to do**

Do not add enterprise infrastructure, bypass failing CI, or deploy production
from a failing/unreviewed branch.

**Dependencies**

Phases 5–8 and a chosen backend runtime.

**Blockers**

Unresolved authorization/runtime/deployment ownership or failing tests.

## Phase 10 — PRODUCTION RELEASE

**Objective**

Publish a traceable production release with rollback information.

**Inputs**

Green CI commit, reviewed data versions, owner approval, Firebase target and
approved backend runtime credentials.

**Files/modules expected to change**

Production deployment record, version metadata and rollback documentation; no
scientific source file should change during a release-only deployment.

**Owner/role**

Release owner; repository owner approves production.

**Tasks**

- Run all CI checks and production build.
- Deploy frontend to Firebase Hosting and backend/API to its selected runtime.
- Run the full smoke matrix from `DEPLOYMENT_RUNBOOK.md`.
- Record production URL, API URL, Firebase project ID, commit SHA, version and
  deployment date.

**Deliverables**

- Production deployment record and rollback instructions.

**Tests**

- Normal, invalid input, q=1, total condenser, partial condenser,
  non-converged, thermo extrapolation, energy and sensitivity smoke tests.

**Definition of Done**

Production is reachable, traceable to a green commit and can be rolled back
with frontend/API/data versions kept compatible.

**What NOT to do**

Do not force-push, deploy with failing tests, expose credentials, or treat a
frontend URL as proof that the Python backend is deployed.

**Dependencies**

Phases 0–9, owner approval and runtime credentials supplied by the owner.

**Blockers**

Any failed CI/smoke test, missing approval, missing Firebase target or missing
backend runtime.

## Current starting point

Phase 0 is frozen and the Phase 1 local skeleton/UI shell is implemented and
verified. The next single action is Phase 2 Firebase target confirmation:
the owner must log in/select the intended Firebase project, after which the
minimum shell can be configured and manually deployed. Scientific Antoine data
review and total-condenser engine work can proceed in parallel, while all
simulation outputs remain explicitly pending until the backend is implemented.
