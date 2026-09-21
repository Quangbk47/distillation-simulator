# Next Session Prompt

Start by running `git pull`, then read these files in order:

1. `docs/PROJECT_RULES.md`
2. `docs/ROADMAP.md` for the phase being considered
3. `docs/PROGRESS.md`
4. the relevant `docs/TODO.md` items
5. the relevant specification files

The repository rule is:

> **NO WORK IS COMPLETE UNTIL PROGRESS IS UPDATED.**

Use the checkpoint sequence `IMPLEMENT → TEST → UPDATE PROJECT DOCUMENTATION
→ COMMIT → PUSH`. Do not call a task `DONE` a phase `DONE`; preserve every
remaining item. Use only `NOT STARTED`, `IN PROGRESS`, `BLOCKED` and `DONE` for
phase status, with `DEFERRED` only as a task/item label.

Current starting point: Phase 0 and Phase 1 are `DONE`; Phase 2 and Phase 3 are
`BLOCKED`; later phases are `NOT STARTED` as recorded in `PROGRESS.md`.

The immediate next action is to confirm the Firebase account and target
project for Phase 2. Firebase work cannot proceed until the owner logs in and
confirms the target project. If login is required, stop and ask the owner;
never create or guess a project and never handle or commit credentials.

Do not invent Antoine or enthalpy data, partial-condenser equations or
validation mappings. Keep partial condenser `NOT_IMPLEMENTED`. Enthalpy is a
Phase 6 blocker only. Before Phase 4, verify the total-condenser closure gate:
outer `xD`, reboiler boundary and direct `NF` stage indexing, with no
geometric-stage rejection gate.
