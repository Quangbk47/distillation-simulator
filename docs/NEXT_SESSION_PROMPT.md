# Next Session Prompt

Pull latest main, then read `PROJECT_RULES.md`, the relevant `ROADMAP.md`
phase, `PROGRESS.md`, `TODO.md`, `HANDOVER.md` and related specifications.

Phase 0/1 are DONE. Phase 2 deployment and smoke gates pass, but the evidence
PR is pending GitHub write access. Phase 3 is BLOCKED by TODO-001.
The static demo is live at https://distillation-simulator.web.app. The prior
Firebase HTTP 403 was resolved for the authorized session on 2026-09-27;
no new project/site is needed. Deployment and smoke evidence are recorded in
`DEPLOYMENT_RUNBOOK.md`. Do not repeat deployment as unfinished work; publish the evidence PR first.

Next action: publish/review/merge the local evidence checkpoint, then close
Phase 2. Afterward, the scientific lead must approve component coefficients, units,
applicable ranges, source citations, reviewer and review date under
`THERMODYNAMIC_DATA_SPEC.md`. Then implement the Phase 3 minimum engine and
reviewed total-condenser closure. Do not invent coefficients or review approval.
Keep partial condenser NOT_IMPLEMENTED and enthalpy as a Phase 6 blocker only.

NO WORK IS COMPLETE UNTIL PROGRESS IS UPDATED. Follow the technical workflow
in PROJECT_RULES: implementation, tests, docs, commit/push, PR, CI/review,
merge, applicable production build/deploy/smoke and evidence. Owner approval
is not a separate technical gate; scientific decisions remain with the expert.
