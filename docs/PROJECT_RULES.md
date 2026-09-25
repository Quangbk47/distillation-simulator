# Project Rules

These rules are binding for V1. Detailed calculation closure is in
`PROCESS_MODEL.md`, formulas in `CALCULATION_FORMULAS.md`, algorithm order in
`ALGORITHM_SPEC.md`, and the UI contract in `UI_UX_SPEC.md`.

## Team workflow

The mandatory repository rule is:

> **NO WORK IS COMPLETE UNTIL PROGRESS IS UPDATED.**

A meaningful technical unit of work follows this sequence:

```text
CODE
→ TEST
→ UPDATE DOCS
→ COMMIT/PUSH
→ PR
→ CI/REVIEW
→ MERGE MAIN
→ DEPLOY FIREBASE PRODUCTION
→ SMOKE TEST
→ UPDATE EVIDENCE
```

The student team may execute this workflow end-to-end without waiting for a
separate Owner approval at each Phase. Owner approval is not a phase blocker.
The PR review and green CI gate still happen before merging to `main`, and the
deployment/smoke-test evidence is required before a phase or release is marked
complete. A documentation-only change must still update the relevant
project-management files, pass its consistency checks, and be committed and
pushed.

This autonomy does not authorize guessing scientific decisions, reviewed data,
Firebase targets, credentials or production secrets. An unresolved scientific
decision remains `BLOCKED` until the designated scientific decision is recorded;
missing access is a blocker only when no authorized account/access path exists.

`TASK DONE` does not mean `PHASE DONE`. A phase remains incomplete until its
entire Definition of Done is satisfied. A completed task inside an incomplete
phase may be marked `DONE`, while the phase remains `IN PROGRESS` or
`BLOCKED`. Work intentionally moved to another phase is labelled `DEFERRED`
on the task/item and recorded in `ROADMAP.md`/`TODO.md`; `DEFERRED` is not a
fifth phase status.

## Allowed status values

Phases use exactly these four primary statuses:

- `NOT STARTED`: work has not begun.
- `IN PROGRESS`: work has begun and in-scope work remains.
- `BLOCKED`: work cannot continue because it awaits an unresolved dependency,
  scientific decision, required data, or authorized access. Lack of a separate
  Owner approval is not sufficient to mark technical work blocked.
- `DONE`: the complete phase Definition of Done is met, required tests pass,
  documentation is current, and the change is committed and pushed.

Tasks may additionally use the label `DEFERRED` when work is deliberately
moved to a later phase. A blocked task is not a failed task; it must record
what is complete, what remains, the blocker, who/what can unblock it, and the
next action after unblocking.

## Source of truth and documentation ownership

- `ROADMAP.md` — where the project is going: phase scope, dependencies,
  ordering and Definitions of Done. It is not a task diary.
- `PROGRESS.md` — where the project is now: current phase status, completed
  work, remaining work, blockers, evidence and next action.
- `TODO.md` — what remains: actionable work, dependencies and acceptance
  conditions. Unresolved TODOs must not be deleted for cosmetic reasons.
- Specification files — how the system must work. Update them only when a
  requirement, scientific decision, formula/algorithm, API/data contract,
  UI contract or test/acceptance contract changes.
- `HANDOVER.md` — what the next person needs to know at a milestone or
  significant handoff.
- `NEXT_SESSION_PROMPT.md` — where the next working session starts; it must
  not describe already-completed work as the next task.

Do not maintain the same fact independently in multiple files in a way that
can diverge. If implementation and specification disagree, first decide
whether the implementation or the source-of-truth specification is wrong;
then update the appropriate source and record a meaningful change in
`PROGRESS.md`/`HANDOVER.md`.

## Required progress and evidence

Update `PROGRESS.md` after every meaningful unit of work: a task or substantial
part is completed, a phase changes status, a blocker appears or is resolved,
work is handed to a later session, or a milestone is reached.

Each phase entry must contain:

```text
Phase
Status
Completed
Remaining
Blockers
Next Action
Evidence
Last Updated
```

`DONE` requires evidence rather than description alone:

- code: relevant tests and commit SHA;
- deployment: build, URL, smoke test and commit SHA;
- scientific/data work: source/citation, reviewer when required and reference
  result;
- UI: build, relevant manual/test verification and commit SHA;
- documentation: files updated, consistency check and commit SHA.

Keep completed and remaining items cumulative. When a later contributor
finishes one remaining item, add it to `Completed` but preserve all other
unfinished items in `Remaining`.

## Before and after a working session

Before coding, every contributor must:

1. `git pull`;
2. read `PROJECT_RULES.md`;
3. read the relevant `ROADMAP.md` phase;
4. read `PROGRESS.md`;
5. read related `TODO.md` items;
6. read the relevant specifications;
7. identify the current `Next Action`;
8. only then change the repository.

Before ending work:

1. run relevant tests/checks;
2. update `PROGRESS.md`;
3. update `TODO.md` for new, deferred or completed work;
4. update `ROADMAP.md` only if scope, dependency, ordering, Definition of Done
   or a major task assignment changes;
5. update specifications only if their contract changes;
6. update `HANDOVER.md` for a milestone, significant handoff or important
   blocker;
7. update `NEXT_SESSION_PROMPT.md` when the next action changes;
8. review `git diff` and `git status`;
9. commit;
10. push;
11. open/update the PR and record the CI/review state;
12. after merge, deploy the applicable production artifact, run the smoke test,
    and update evidence with commit SHA, build ID, URL, date and result;
13. confirm that the commit and evidence exist on the remote.

One meaningful commit should include implementation, related tests and the
progress update when practical. Do not create a cosmetic progress-only commit
immediately after implementation if the files could have been updated in the
same checkpoint.

## V1 technical rules

- System: binary Ethanol–Water, steady-state, constant pressure.
- Runtime VLE: Raoult + Antoine only. Wilson/NRTL is not a V1 runtime feature.
- `q` is a direct finite numeric input; do not infer it from `Tfeed`.
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
