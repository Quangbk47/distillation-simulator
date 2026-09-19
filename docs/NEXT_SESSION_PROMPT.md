# Next Session Prompt

Continue Distillation Simulator from `docs/ROADMAP.md` and
`docs/PROJECT_AUDIT.md`. Current status is Phase 1 local readiness: the
dependency-free UI shell builds and the API health/version endpoints run, but
there is no production calculation engine, reviewed thermo data or Firebase
configuration.

Read `README.md`, `PROJECT_RULES.md`, `EXPERT_DECISIONS.md`,
`CALCULATION_FORMULAS.md`, `ALGORITHM_SPEC.md`, `PROGRESS.md` and the relevant
phase before coding. Do not invent unresolved thermo/energy decisions. Keep
engine separate from UI; every output must be computed and tested. Firebase
Hosting is frontend-only and must not be treated as a Python backend runtime.

Start with the first incomplete roadmap task. Before Phase 4, verify the
Calculation Closure Gate: xD outer solve, reboiler boundary and direct NF stage
indexing. Do not invent partial-condenser equations; keep that branch
NOT_IMPLEMENTED until expert decisions are recorded. Enthalpy review is only a
Phase 6 blocker. If Firebase login/project confirmation is required, stop and
ask the owner to complete it; never handle or commit credentials.
