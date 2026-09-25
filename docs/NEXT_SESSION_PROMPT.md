# Next Session Prompt

Start by running `git pull`, then read these files in order:

1. `docs/PROJECT_RULES.md`
2. `docs/ROADMAP.md` for the phase being considered
3. `docs/PROGRESS.md`
4. the relevant `docs/TODO.md` items
5. the relevant specification files

The repository rule is:

> **NO WORK IS COMPLETE UNTIL PROGRESS IS UPDATED.**

Use the checkpoint sequence `READ CURRENT STATE → IMPLEMENT → TEST → UPDATE
DOCS → COMMIT/PUSH → PR → CI/REVIEW → MERGE MAIN → BUILD PRODUCTION → DEPLOY
FIREBASE HOSTING → PRODUCTION SMOKE TEST → UPDATE EVIDENCE → CLOSE PHASE IF DoD
PASSES → CONTINUE NEXT PHASE`. Do not call a task `DONE` a phase `DONE`; preserve
every remaining item. Use only `NOT STARTED`, `IN PROGRESS`, `BLOCKED` and
`DONE` for phase status, with `DEFERRED` only as a task/item label.

Current starting point: Phase 0/1 DONE, Phase 2 IN PROGRESS, Phase 3 BLOCKED.
The legacy Firebase target `distillation-simulator` returns HTTP 403 to the
current CLI session. Create/select a student-controlled Firebase project/site,
update `.firebaserc`/`firebase.json`, deploy production, smoke-test the public
URL and update evidence. No separate Owner approval is required for any of
these technical steps. Do not mark Phase 2 DONE until deployment and smoke
tests pass. See `DEPLOYMENT_RUNBOOK.md` for commands.

Do not invent Antoine or enthalpy data, partial-condenser equations or
validation mappings. Keep partial condenser `NOT_IMPLEMENTED`. Enthalpy is a
Phase 6 blocker only. Before Phase 4, verify the total-condenser closure gate:
outer `xD`, reboiler boundary and direct `NF` stage indexing, with no
geometric-stage rejection gate.
