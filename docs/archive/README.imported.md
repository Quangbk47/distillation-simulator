# Distillation Simulator

> **Historical import only.** This file is preserved as evidence of the
> original material and is not an implementation, workflow or scientific source
> of truth. Do not use it to override `PROJECT_RULES.md`, `EXPERT_DECISIONS.md`,
> `PROCESS_MODEL.md` or the current Firebase/deployment workflow. Technical
> work is student-owned; unresolved scientific decisions remain blocked until
> the designated scientific lead/expert records a decision.

Mô phỏng chưng cất nhị phân steady-state, Ethanol–Water V1; phục vụ học tập, nghiên cứu, validation; không phải Aspen/HYSYS thu nhỏ.

V1: McCabe–Thiele; Antoine + Raoult, Wilson khi duyệt. Input F/zF/q/P/N/NF/condenser/heat loss/R/D. Output xD/xB/D/B/Recovery/QC/QR/residual. Sensitivity một biến R/N/NF.

Đọc PROJECT_RULES → EXPERT_DECISIONS → PROCESS_MODEL → ALGORITHM_SPEC trước khi code.
