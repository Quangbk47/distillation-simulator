# TODO — execution queue

This file contains unresolved work only. A task can be `DONE` while its phase
remains `IN PROGRESS`; phase status is tracked in `PROGRESS.md`. Do not delete
an unresolved item to make the queue look clean.

## P0 — blockers and decisions

### TODO-001 — Review Antoine records

- Phase: 3/4
- Status: `BLOCKED`
- Owner/role: Scientific lead
- Dependency/blocker: Component, units, ranges, citation, reviewer and review
  date are not approved.
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
- Dependency/blocker: Cp/latent-heat sources and reviewer approval are
  missing.
- Acceptance condition: Sources, reference state, sign convention, ranges and
  reviewer/date are recorded and `calcEnergy` reference tests pass.

### TODO-004 — Confirm Firebase target

- Phase: 2
- Status: `BLOCKED`
- Owner/role: Repository owner / deployment owner
- Dependency/blocker: Owner Firebase login and target project selection.
- Acceptance condition: Owner confirms account and project ID; configuration
  can be added without guessing or committing credentials.

### TODO-005 — Choose backend runtime

- Phase: 9/10
- Status: `NOT STARTED`
- Owner/role: Project owner / DevOps
- Dependency/blocker: Functional backend and deployment constraints.
- Acceptance condition: A separate Python API runtime is selected and its
  deploy/smoke-test procedure is documented.

## P1 — implementation sequence

### TODO-007 — Implement minimum calculation engine

- Phase: 3
- Status: `BLOCKED`
- Owner/role: Student developer
- Dependency/blocker: TODO-001 reviewed Antoine data.
- Acceptance condition: VLE, bubble temperature, balances, recovery and
  residual gates pass the relevant tests without fabricated values.

### TODO-008 — Complete calculation closure

- Phase: 3/4
- Status: `BLOCKED`
- Owner/role: Student developer with scientific reviewer
- Dependency/blocker: TODO-001 and TODO-007.
- Acceptance condition: Total-condenser outer `xD` solve, reboiler boundary,
  direct `NF` section switch and reference residuals pass; no `NF_geo` gate is
  introduced.

### TODO-009 — Implement McCabe–Thiele path

- Phase: 4
- Status: `NOT STARTED`
- Owner/role: Student developer
- Dependency/blocker: TODO-008.
- Acceptance condition: q-line, operating lines, stepping, `N/NF`, total
  condenser and both section branches have tested outputs; partial condenser
  remains unavailable until TODO-002 is complete.

### TODO-010 — Connect functional UI

- Phase: 5
- Status: `NOT STARTED`
- Owner/role: Student developer
- Dependency/blocker: TODO-009 and API contract completion.
- Acceptance condition: UI consumes backend results, warnings and stage data;
  no client-side scientific authority or fake result is introduced.

### TODO-011 — Implement sensitivity

- Phase: 7
- Status: `NOT STARTED`
- Owner/role: Student developer
- Dependency/blocker: Validated base simulation and API/UI path.
- Acceptance condition: Each sweep changes exactly one of `R`, `N` or `NF` and
  preserves all other inputs; tests cover the contract.

## P2 — release and validation

### TODO-012 — Scientific validation

- Phase: 8
- Status: `NOT STARTED`
- Owner/role: Scientific lead and validation owner
- Dependency/blocker: Reviewed source/mapping and completed calculation path.
- Acceptance condition: Reference/literature case is reviewed, executed and
  reported using the accepted MAE threshold of 5 percentage points.

### TODO-013 — Firebase static hosting

- Phase: 2/5/10
- Status: `BLOCKED`
- Owner/role: Deployment owner
- Dependency/blocker: TODO-004, then owner-managed login and target access.
- Acceptance condition: Static build is deployed, URL and commit are recorded,
  and a smoke test passes; no credentials are committed.

### TODO-014 — Product hardening and production release

- Phase: 9/10
- Status: `NOT STARTED`
- Owner/role: Team / DevOps
- Dependency/blocker: Earlier phases, TODO-005 and deployment access.
- Acceptance condition: CI/release protections, backend runtime, frontend
  hosting, production smoke test and release evidence are complete.
