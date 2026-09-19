# Progress

2026-09-18 — Expert confirmation integrated: 1A,2C,3B,4A,5B,6A,7A,8C,9C,10A,11B,12C,13B.

2026-09-18 — Repository organized into docs/data/src/tests boundaries. Added Python API/engine skeleton, explicit Raoult–Antoine and residual contracts, pending thermodynamic/validation data schemas, local development files and GitHub Actions CI. No production simulation engine or deployment was added.

2026-09-18 — Project decision accepted the question 10A validation threshold: primary metric `MAE_xD_xB_percentage_points`, threshold `5` percentage points. This is recorded in `VALIDATION_ACCEPTANCE.md`.

2026-09-19 — Project audit and roadmap hardening completed. Added a requirement
matrix, explicit source-of-truth hierarchy, Phase 0–10 execution contract,
early/iterative Firebase milestones, and clarified that Firebase Hosting serves
frontend/static assets while the Python API needs a separate runtime. No
Firebase project was selected or credentials handled.

Current phase: Phase 1 local readiness. The repository has a tested backend
skeleton and a static UI shell, but is not yet a working simulator. The next
deployment task is Firebase target confirmation for Phase 2.

2026-09-19 — Phase 1 implementation advanced: added a dependency-free static
UI shell in `web/`, a reproducible `scripts/build_frontend.py` build, and a CI
frontend-build step. The local backend served `/health` and thermo-version with
HTTP 200; the built frontend served HTTP 200 and visibly reported
`ENGINE NOT CONNECTED`/`NOT CALCULATED`. No scientific values are fabricated.

Phase 1 is locally ready. Phase 2 is blocked only at Firebase project/account
confirmation and login; do not guess a project or create credentials.

Remaining blockers: reviewed Antoine data for Phase 3/4, the partial-condenser
reference convention/case, validation source/mapping review, Firebase project
and login confirmation, and a separate backend deployment runtime. Reviewed
enthalpy data is a Phase 6 blocker only; it does not block Phase 3/4 VLE/stage
work.
