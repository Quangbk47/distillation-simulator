# Handover

## Current Phase

Phase 2 — FIREBASE EARLY CONNECTION

## Current Status

`BLOCKED`. Phase 0 and Phase 1 are `DONE`. Phase 2 is `BLOCKED`; Phase 3 is `BLOCKED`;
later phases are `NOT STARTED` unless recorded otherwise in `PROGRESS.md`.

## What is completed

- V1 contracts and direct-`NF` section-switch convention are documented.
- Backend/API skeleton, tests and local development commands exist.
- Dependency-free static UI shell and reproducible frontend build exist.
- Local structure, formatting, lint, type-check, tests, package build, secret
  scan, backend health and static frontend checks pass.
- Phase 1 is complete: GitHub Actions run `35499694516` passed at
  `86a0a1768ac50c926c83dd032ef7022c46e262ea`; the full local gate passed again
  on 2026-09-21, including 11 tests.
- PR #2 was reviewed, passed CI run `36154667511` and merged to `main` as
  `bc4d2e5e07451c8d9d8c18e4f23f633fa3e99b52`.
- The production frontend artifact was built with ID
  `3739c85b7628bc20cd6d5e7aea1bfe42a81a2792beddeb0e5e175c52760cea20`.
- Total condenser remains the primary path; partial condenser remains
  `NOT_IMPLEMENTED`.

## What remains

- Review Antoine data before Phase 3/4 scientific output.
- Implement the minimum calculation engine and closure gate.
- Restore Firebase project/site access, finish Phase 2 deployment and run the
  public smoke verification.
- Keep all unresolved items in `PROGRESS.md` and `TODO.md`.

## Known blockers

- Firebase target is configured as `distillation-simulator`, but the current
  CLI session receives project/site permission failure (HTTP 403); no
  production URL exists.
- Reviewed Antoine records block Phase 3/4 scientific implementation.
- Partial-condenser equations/reference case are `DEFERRED` and blocked by a
  scientific decision.
- Reviewed enthalpy data blocks Phase 6 only.
- A separate backend runtime is required; Firebase Hosting is frontend-only.

## Important decisions

- `ROADMAP.md` describes where the project is going; `PROGRESS.md` describes
  where it is; `TODO.md` describes what remains.
- `TASK DONE` is not `PHASE DONE`.
- The mandatory rule is **NO WORK IS COMPLETE UNTIL PROGRESS IS UPDATED**.
- A phase uses only `NOT STARTED`, `IN PROGRESS`, `BLOCKED` or `DONE`.
- Work intentionally moved later is labelled `DEFERRED`, never used as a phase
  status.
- Never guess scientific data, Firebase projects or credentials.

## Files/modules involved

- Project management: `docs/PROJECT_RULES.md`, `docs/ROADMAP.md`,
  `docs/PROGRESS.md`, `docs/TODO.md`, `docs/NEXT_SESSION_PROMPT.md`.
- Contracts: `docs/PROCESS_MODEL.md`, `docs/ALGORITHM_SPEC.md`,
  `docs/CALCULATION_FORMULAS.md`, `docs/DATA_MODEL.md`.
- Runtime skeleton: `src/`, `api/`, `tests/`.
- Static shell: `web/`, `scripts/build_frontend.py`.

## Last verified commit

`bc4d2e5e07451c8d9d8c18e4f23f633fa3e99b52` — PR #2 merge commit; CI run
`36154667511` passed. Firebase deployment was attempted on 2026-09-25 but
failed before upload because the project was inaccessible.

## Next recommended action

Read `PROGRESS.md` and `DEPLOYMENT_RUNBOOK.md`. Phase 2 configuration is ready.
Restore authorized access to `distillation-simulator`, run
`firebase deploy --only hosting --project distillation-simulator
--non-interactive`, verify the public URL and record evidence. Do not mark
Phase 2 `DONE` until deployment and smoke tests pass. No separate Owner
approval is required at a Phase boundary. Credentials remain outside the repo.
