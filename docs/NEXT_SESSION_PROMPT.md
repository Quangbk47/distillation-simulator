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

Current starting point: Phase 0/1 DONE, Phase 2 IN PROGRESS, Phase 3 BLOCKED.
The Firebase target `distillation-simulator` and CLI login are confirmed.
Finish CI, deploy Hosting only, smoke-test the public URL and update evidence.
Use a PR: `CI_REQUIREMENTS.md` requires reviewer approval and green checks
before merge to main. See `DEPLOYMENT_RUNBOOK.md` for commands.

Do not invent Antoine or enthalpy data, partial-condenser equations or
validation mappings. Keep partial condenser `NOT_IMPLEMENTED`. Enthalpy is a
Phase 6 blocker only. Before Phase 4, verify the total-condenser closure gate:
outer `xD`, reboiler boundary and direct `NF` stage indexing, with no
geometric-stage rejection gate.
