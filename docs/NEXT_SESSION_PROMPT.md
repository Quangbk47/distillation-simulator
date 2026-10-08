# Next Session Prompt

Pull latest main, then read `PROJECT_RULES.md`, the relevant `ROADMAP.md`
phase, `PROGRESS.md`, `TODO.md`, `HANDOVER.md` and related specifications.

Phase 0/1/2 are DONE. Phase 3 is DONE for the reviewed Ethanol-Water
Raoult-Antoine minimum engine. Phase 4/5 are IN PROGRESS for total-condenser
McCabe-Thiele and the local functional UI. Scientific validation still needs a
GVHD-approved golden/reference case.
Firebase now uses the account-owned project/site `delta-pagoda-509904-j8`
under `bichloannb06@gmail.com`. The deployed URL is
https://delta-pagoda-509904-j8.web.app and its browser metadata reports project
`delta-pagoda-509904-j8` with build
`70f1fd3097ee0c74c9238c6db58eac3d444593485167086c957d54ca5e6181f7`. Do not
use another person's Firebase project for future phases.

Next action: continue safe Phase 4/5 hardening and local UI/API checks while
waiting for GVHD to confirm an authoritative validation case. The approved
Antoine runtime dataset is already committed; do not replace it or add other
Water records without review. Do not claim the supervisor-form candidate as a
PASS because its displayed D/xD/xB/recovery values are not mutually consistent
under the recorded mapping. Keep partial condenser NOT_IMPLEMENTED and enthalpy
as a Phase 6 blocker only.

NO WORK IS COMPLETE UNTIL PROGRESS IS UPDATED. Follow the technical workflow
in PROJECT_RULES: implementation, tests, docs, commit/push, PR, CI/review,
merge, applicable production build/deploy/smoke and evidence. Owner approval
is not a separate technical gate; scientific decisions remain with the expert.
