# TODO — execution queue

## P0 — unblock the critical path

- Scientific lead: review Antoine records and approve component/units/ranges,
  citation, reviewer and date.
- Scientific lead: review Cp/latent-heat sources and confirm the energy
  reference/sign convention already written in `CALCULATION_FORMULAS.md`.
- Owner: confirm Firebase project ID, account/login and frontend hosting target;
  do not create or guess a project.
- Team: keep Phase 0 decisions and `docs/PROJECT_AUDIT.md` synchronized.

## P1 — implementation sequence

- Skeleton: keep local app, CI, lint, type-check, tests and build green.
- Firebase: add minimum static status UI and early hosting deploy after target
  confirmation.
- Core: implement Antoine/Raoult, bubble temperature, material/component
  balance, recovery and residual gates.
- McCabe–Thiele: implement q-line, operating lines, stepping, N/NF and both
  condenser branches with separate tests.
- UI: direct q, absolute heat loss, warnings, results, stage table, column
  diagram and basic graph.
- Energy: implement pure `calcEnergy` with reviewed data.
- Sensitivity: implement one-variable R/N/NF sweeps.

## P2 — release hardening

- Validation: review and evaluate a literature/experimental case using the
  accepted MAE threshold only after source/mapping review.
- DevOps: protect `main`, add staging/iterative Firebase deployment after CI,
  choose and document separate backend runtime, then run production smoke
  tests.
