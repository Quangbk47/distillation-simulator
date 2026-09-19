# Project Rules

These rules are binding for V1. Detailed calculation closure is in
`PROCESS_MODEL.md`, formulas in `CALCULATION_FORMULAS.md`, algorithm order in
`ALGORITHM_SPEC.md`, and the UI contract in `UI_UX_SPEC.md`.

- System: binary Ethanol–Water, steady-state, constant pressure.
- Runtime VLE: Raoult + Antoine only. Wilson/NRTL is not a V1 runtime feature.
- q is a direct finite numeric input; do not infer it from `Tfeed`.
- `N` counts body trays only; condenser and reboiler are excluded.
- Total and partial condenser belong to V1. Total is closed now; partial is
  `OPEN/BLOCKING` and must return `NOT_IMPLEMENTED` until approved equations
  and a reference case exist.
- Normal simulation input uses `0 < zF < 1` and `0 < D_kmol_h < F_kmol_h`;
  pure-component limits are VLE tests.
- `heatLoss_kW` is an absolute non-negative kW load.
- Success requires physical checks plus total-mass, ethanol-balance, outer and
  solver residuals strictly `< 1e-4`.
- Extrapolation is allowed only with structured warning/provenance.
- Backend/API is the production authority; no secret or authoritative data is
  placed in the client.
- Sensitivity changes exactly one of `R`, `N` or `NF` and preserves all other
  inputs.
- Validation uses the latest decision in `VALIDATION_ACCEPTANCE.md`: MAE of
  xD/xB in percentage points, threshold 5, only after source review.
- Do not add AI/ML, optimization, dynamic simulation, detailed hydraulics,
  microservices, Kubernetes or enterprise architecture.
