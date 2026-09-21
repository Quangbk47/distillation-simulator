# Handover

## Current Phase

Phase 2 — FIREBASE EARLY CONNECTION

## Current Status

`BLOCKED`. Phase 0 and Phase 1 are `DONE`. Phase 2 and Phase 3 are `BLOCKED`;
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
- Total condenser remains the primary path; partial condenser remains
  `NOT_IMPLEMENTED`.

## What remains

- Review Antoine data before Phase 3/4 scientific output.
- Implement the minimum calculation engine and closure gate.
- Confirm Firebase account/project before any hosting configuration.
- Keep all unresolved items in `PROGRESS.md` and `TODO.md`.

## Known blockers

- Firebase owner login and target project selection block Phase 2 deployment.
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

`86a0a1768ac50c926c83dd032ef7022c46e262ea` — Phase 1 checkpoint, with green
GitHub Actions run `35499694516`.

## Next recommended action

The next contributor must first run `git pull`, read `PROJECT_RULES.md`,
`ROADMAP.md` for the relevant phase, `PROGRESS.md`, relevant `TODO.md` items,
and the relevant specifications. Phase 1 is complete. The immediate external
blocker is owner Firebase login/project confirmation; if login is required,
stop and ask the owner to complete it. Do not begin Firebase configuration,
calculation implementation or deployment until its prerequisites are met.
