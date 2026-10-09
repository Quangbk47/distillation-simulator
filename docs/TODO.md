# TODO — execution queue

This file contains unresolved work only. A task can be `DONE` while its phase
remains `IN PROGRESS`; phase status is tracked in `PROGRESS.md`. Do not delete
an unresolved item to make the queue look clean.

## P0 — blockers and decisions

### TODO-001 — Review Antoine records

- Phase: 3/4
- Status: `DONE`
- Owner/role: Scientific lead
- Dependency/blocker: Resolved by GVHD approval on 2026-10-04.
- Acceptance condition: Reviewed records are committed in the agreed schema;
  provenance and applicable ranges are explicit; reference tests consume the
  approved records.

### TODO-002 — Decide partial-condenser contract

- Phase: 4/5
- Status: `BLOCKED`
- Label: `DEFERRED`
- Owner/role: Scientific lead
- Dependency/blocker: Approved equations and a reviewed golden case are
  missing.
- Acceptance condition: Equations, API behavior, reference case and tests are
  approved; until then the branch remains `NOT_IMPLEMENTED`.

### TODO-003 — Review energy data and sign convention

- Phase: 6
- Status: `BLOCKED`
- Owner/role: Phase 6 scientific owner
- Dependency/blocker: Cp/latent-heat sources and designated scientific review are
  missing.
- Acceptance condition: Sources, reference state, sign convention, ranges and
  reviewer/date are recorded and `calcEnergy` reference tests pass.
- Progress: Guardrail tests now assert that `calc_energy` raises
  `EnergyCalculationNotReady` and that API `QC_kW`, `QR_kW` and
  `energyBreakdown` remain null instead of fabricated before review.

### TODO-005 — Choose backend runtime

- Phase: 9/10
- Status: `NOT STARTED`
- Owner/role: Student developer / DevOps
- Dependency/blocker: Functional backend and deployment constraints.
- Acceptance condition: A separate Python API runtime is selected and its
  deploy/smoke-test procedure is documented.

## P1 — implementation sequence

### TODO-007 — Implement minimum calculation engine

- Phase: 3
- Status: `DONE`
- Owner/role: Student developer
- Dependency/blocker: TODO-001 resolved.
- Acceptance condition: VLE, bubble temperature, balances, recovery and
  residual gates pass the relevant tests without fabricated values.

### TODO-008 — Complete calculation closure

- Phase: 3/4
- Status: `IN PROGRESS`
- Owner/role: Student developer with scientific reviewer
- Dependency/blocker: Numerical reference cases and residual validation.
- Acceptance condition: Total-condenser outer `xD` solve, reboiler boundary,
  direct `NF` section switch and reference residuals pass; no `NF_geo` gate is
  introduced.
- Progress: Outer residual gate is enforced and non-converged cases return
  a structured `failed` result instead of clamped values or an unstructured API
  exception. Local smoke passes from input through xD/xB/recovery/D/B and
  warning details. API guardrail tests now reject unapproved extra fields,
  `NF > N`, `D >= F`, invalid boundary values and unknown condenser values;
  golden/reference validation is still required.

### TODO-009 — Implement McCabe–Thiele path

- Phase: 4
- Status: `IN PROGRESS`
- Owner/role: Student developer
- Dependency/blocker: TODO-008 validation remains.
- Acceptance condition: q-line, operating lines, stepping, `N/NF`, total
  condenser and both section branches have tested outputs; partial condenser
  remains unavailable until TODO-002 is complete.
- Progress: q-line, feed intersection, rectifying/stripping lines, stage table
  and graph-ready response are implemented for total condenser. Local UI smoke
  rendered the McCabe--Thiele plot and stage data. Unit tests now lock the
  direct `NF` section switch, stage numbering and reflux-ratio response for a
  converged total-condenser case. Partial condenser remains `NOT_IMPLEMENTED`.

### TODO-010 — Connect functional UI

- Phase: 5
- Status: `IN PROGRESS`
- Owner/role: Student developer
- Dependency/blocker: TODO-009 and API contract completion.
- Acceptance condition: UI consumes backend results, warnings and stage data;
  no client-side scientific authority or fake result is introduced.
- Progress: Simulation tab consumes backend output and renders xD/xB/recovery,
  stage table, McCabe--Thiele plot and detailed thermodynamic warnings from API
  data. Non-converged total-condenser cases now show a structured failed status
  and explanatory error message instead of a generic API failure. The frontend
  also suppresses invalid stage-table/plot claims for failed results and gives
  separate visual states for success, warning, failed and calculating.
  Sensitivity remains disabled.

### TODO-011 — Implement sensitivity

- Phase: 7
- Status: `NOT STARTED`
- Owner/role: Student developer
- Dependency/blocker: Validated base simulation and API/UI path.
- Acceptance condition: Each sweep changes exactly one of `R`, `N` or `NF` and
  preserves all other inputs; tests cover the contract.
- Progress: The endpoint remains intentionally disabled, but it now returns a
  structured `NOT_IMPLEMENTED` response that explains sensitivity is reserved
  until the base case has an approved validation case.

## P2 — release and validation

### TODO-012 — Scientific validation

- Phase: 8
- Status: `IN PROGRESS`
- Owner/role: Scientific lead and validation owner
- Dependency/blocker: Reviewed source/mapping and completed calculation path.
- Acceptance condition: Reference/literature case is reviewed, executed and
  reported using the accepted MAE threshold of 5 percentage points.
- Progress: Validation request and pending case template are prepared in
  `docs/VALIDATION_REQUEST.md` and
  `data/validation/cases/ethanol-water.pending.json`. A registration/scope note
  is recorded in `docs/PROJECT_REGISTRATION.md` to keep the broad project title
  aligned with the narrow approved V1 implementation. The supervisor-form
  candidate values have been entered with the scientifically reasonable mapping
  `bottom purity 94.8 mol% water -> xB_ethanol = 0.052`; however, the current
  engine does not converge for the candidate input (`D=45.2`, `R=2`, `N=20`,
  `NF=10`). A direct material-balance check also shows the displayed `D`,
  `xD`, mapped `xB` and recovery are not mutually consistent, so no validation
  PASS is claimed until GVHD confirms which value is authoritative or provides a
  mass-balanced reference case.

### TODO-013 — Firebase evidence and later releases

- Phase: 2/5/10 (Phase 2 deployment/smoke verified on 2026-09-27).
- Status: `IN PROGRESS`
- Owner/role: Student developer / DevOps
- Phase 2 deployment and browser smoke passed at
  https://delta-pagoda-509904-j8.web.app (build
  `70f1fd3097ee0c74c9238c6db58eac3d444593485167086c957d54ca5e6181f7`).
  Reverified on 2026-10-04: asset equality, 404 routes, browser smoke and all
  local quality gates pass. Remaining: publish the committed branch using a
  write-authorized GitHub session, PR CI/review/merge, then deploy and verify
  the green merged source.
- Dependency/blocker: Validated API/UI for Phase 5 and full release gates for
  Phase 10. Existing project/site access and static demo are verified.
- Acceptance condition: Deploy the functional UI and final release after their
  respective CI/review gates; record source/build/URL and smoke evidence.
- Phase 2 evidence: `DEPLOYMENT_RUNBOOK.md`, https://delta-pagoda-509904-j8.web.app.

### TODO-014 — Product hardening and production release

- Phase: 9/10
- Status: `NOT STARTED`
- Owner/role: Team / DevOps
- Dependency/blocker: Earlier phases, TODO-005 and deployment access.
- Acceptance condition: CI/release protections, backend runtime, frontend
  hosting, production smoke test and release evidence are complete.
