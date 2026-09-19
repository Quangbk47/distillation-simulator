# Progress

2026-09-18 — Expert confirmation integrated: 1A,2C,3B,4A,5B,6A,7A,8C,9C,10A,11B,12C,13B.

2026-09-18 — Repository organized into docs/data/src/tests boundaries. Added Python API/engine skeleton, explicit Raoult–Antoine and residual contracts, pending thermodynamic/validation data schemas, local development files and GitHub Actions CI. No production simulation engine or deployment was added.

2026-09-18 — Project decision accepted the question 10A validation threshold: primary metric `MAE_xD_xB_percentage_points`, threshold `5` percentage points. This is recorded in `VALIDATION_ACCEPTANCE.md`.

2026-09-19 — Project audit and roadmap hardening completed. Added a requirement
matrix, explicit source-of-truth hierarchy, Phase 0–10 execution contract,
early/iterative Firebase milestones, and clarified that Firebase Hosting serves
frontend/static assets while the Python API needs a separate runtime. No
Firebase project was selected or credentials handled.

Current phase: Phase 0/1 readiness. The repository is a tested skeleton, not a
working simulator. The first implementation task is the Phase 1 minimum app
and CI verification, followed by Firebase target confirmation for Phase 2.

Remaining blockers: reviewed Antoine and enthalpy data, a partial-condenser
reference convention/case, validation source/mapping review, Firebase project
and login confirmation, and a separate backend deployment runtime.
