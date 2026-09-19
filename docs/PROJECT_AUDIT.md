# Project Audit — V1 Roadmap Hardening

Ngày audit: 2026-09-19
Phạm vi: repository `Quangbk47/distillation-simulator`, branch `main`.

## Kết luận điều hành

Repository hiện là một skeleton có ranh giới module, API contract, schema dữ
liệu, test contract và CI cơ bản. Chưa có calculation engine chạy được, UI
hoàn chỉnh, dữ liệu Antoine/enthalpy đã review, Firebase configuration hoặc
deployment workflow. Vì vậy dự án chưa ở trạng thái sẵn sàng cho người dùng,
nhưng sinh viên có thể bắt đầu từ Phase 0/1 sau khi tuân thủ các blocker trong
`ROADMAP.md`.

Roadmap cũ chỉ có bốn câu mô tả phase, không đủ để giao việc tuần tự và không
đưa Firebase vào giai đoạn sớm. Roadmap mới dùng Phase 0–10, có early
deployment ở Phase 2 và iterative deployment ở Phase 5. Sau vòng audit này,
calculation closure, NF behavior, UI semantics và pending golden cases cũng
được khóa/đánh dấu rõ.

## Source-of-truth hierarchy

1. `EXPERT_CONFIRMATION.md` và `PROJECT_RULES.md` cho quyết định chuyên môn
   đã chốt.
2. `VALIDATION_ACCEPTANCE.md` là quyết định cập nhật sau đó cho metric/ngưỡng
   validation còn bỏ ngỏ trong phiếu gốc.
3. `CALCULATION_FORMULAS.md` và `ALGORITHM_SPEC.md` là calculation contract;
   khi khác source-of-truth ở trên, phải ghi issue và cập nhật contract, không
   tự chọn trong code.
4. `PROCESS_MODEL.md`, `DATA_MODEL.md`, `UI_UX_SPEC.md`, architecture,
   test/validation và deployment docs triển khai các contract đó.
5. `docs/archive/` là lịch sử, không phải authority runtime.

## Requirement consistency matrix

| Requirement | Source of truth | Current implementation | Test/evidence | Status | Action required |
|---|---|---|---|---|---|
| Ethanol–Water | `PROJECT_SCOPE.md`, `EXPERT_CONFIRMATION.md` | Input/domain docs only | Contract tests only | PARTIAL | Keep as the sole V1 system; add engine/reference tests. |
| Raoult + Antoine | `PROJECT_RULES.md`, `ALGORITHM_SPEC.md` | `antoine_raoult.py` has pure helpers; no dataset/runtime engine | `test_antoine_extrapolation...` | PARTIAL | Review data and wire VLE engine. |
| Antoine coefficients | `THERMODYNAMIC_DATA_SPEC.md`, data schema | `records: []`, `PENDING_REVIEW` | JSON schema test | BLOCKED | Select citation, units, temperature range, reviewer/date. |
| VLE | `CALCULATION_FORMULAS.md` §5 | No VLE curve/bubble solver | None | MISSING | Implement and add golden tests. |
| Bubble temperature | `CALCULATION_FORMULAS.md` §5.1 | Not implemented | None | MISSING | Add bracketed root solver and endpoint tests. |
| McCabe–Thiele | `ALGORITHM_SPEC.md` | `solve_mccabe_thiele` raises `NotImplementedError` | None | MISSING | Implement after VLE/material balance. |
| q-line | `CALCULATION_FORMULAS.md` §10 | Only `q` accepted as a field | No q-line test | MISSING | Implement q≠1 and explicit q=1 branch. |
| Rectifying line | `CALCULATION_FORMULAS.md` §9 | Not implemented | None | MISSING | Add slope/intercept tests. |
| Stripping line | `CALCULATION_FORMULAS.md` §12 | Not implemented | None | MISSING | Define singularity/pinch behavior and tests. |
| N convention | `EXPERT_CONFIRMATION.md` | `N`/`NF` contract fields exist | `NF > N` test | ALIGNED CONTRACT | Add stage-count integration test; no condenser/reboiler in N. |
| NF | `PROCESS_MODEL.md`, `DATA_MODEL.md` | Range `1..N` validated | `test_feed_stage...` | ALIGNED CONTRACT | Validate consistency with feed intersection in engine. |
| Total condenser | `EXPERT_CONFIRMATION.md` | Mode accepted; no branch | Mode acceptance only | PARTIAL | Implement and reference-test. |
| Partial condenser | `EXPERT_CONFIRMATION.md`, `PROCESS_MODEL.md` | Mode accepted; formulation is intentionally open | Explicit 501/API test | OPEN/BLOCKING | Ask scientific lead to choose phase/product convention, equations, stage count, residual and golden case; keep `NOT_IMPLEMENTED`. |
| Material balance | `PROCESS_MODEL.md`, formulas §6 | No engine calculation | No balance test | MISSING | Implement F=D+B and reject physical violations. |
| Ethanol balance | `PROCESS_MODEL.md`, formulas §6.2 | No engine calculation | No balance test | MISSING | Implement normalized component residual. |
| Recovery | formulas §7 | No engine calculation | None | MISSING | Use `D*xD/(F*zF)`, guard zero ethanol feed. |
| Stage temperature | formulas §14 | No stage solver | None | MISSING | Calculate from bubble-point relation, never linear fake data. |
| QC | formulas §18 | `calcEnergy` reserved and raises | None | MISSING/BLOCKED | Review Cp/latent heat and implement signed convention. |
| QR | formulas §18 | `calcEnergy` reserved and raises | None | MISSING/BLOCKED | Implement from overall energy balance and fixture tests. |
| heatLoss_kW | `PROJECT_RULES.md` | Schema accepts non-negative absolute kW | Contract test | ALIGNED CONTRACT | Add API/engine negative and effect-on-QR tests. |
| Residual `< 1e-4` | `PROJECT_RULES.md`, formulas §20 | `Residuals` gate now includes mass/component/outer/solver | `test_all_residuals...` | ALIGNED CONTRACT | Return all four residuals from real engine and test each failure path. |
| Warnings | `THERMODYNAMIC_DATA_SPEC.md`, UI spec | Antoine helper returns code only | Extrapolation unit test | PARTIAL | Include component, actual T and source range in API/UI. |
| Extrapolation | `PROJECT_RULES.md` | Helper marks extrapolation | Unit test | PARTIAL | Add physical rejection and smoke test. |
| Sensitivity R | formulas §22 | Parameter validation only | None | MISSING | Implement one-variable sweep and output series. |
| Sensitivity N | formulas §22 | Parameter validation only | None | MISSING | Implement integer validation and sweep tests. |
| Sensitivity NF | formulas §22 | Parameter validation only | None | MISSING | Implement range validation and fixed-input preservation tests. |
| API | `SOFTWARE_ARCHITECTURE.md`, `DATA_MODEL.md` | FastAPI health/version; total is placeholder; partial is explicit 501 | API contract tests | PARTIAL | Wire engine, typed result, auth decision, provenance. |
| UI | `UI_UX_SPEC.md`, `src/ui/README.md` | Placeholder README only | None | MISSING | Build minimum input→run→output UI in Phase 2/5. |
| Testing | `CI_REQUIREMENTS.md`, `TEST_CASES.md` | Unit/integration/reference/pending validation tests | CI config | PARTIAL | Add engine, energy, condenser, smoke and golden tests. |
| Validation | `VALIDATION_PLAN.md`, `VALIDATION_ACCEPTANCE.md` | Pending case and schema; no reviewed source | Pending tests | BLOCKED | Review literature case and only then evaluate/pass. |
| Deployment | `DEPLOYMENT_RUNBOOK.md` | No deployment files/workflow | Repository inventory | MISSING | Establish backend/frontend separation and release gates. |
| Firebase Hosting | user brief, `DEPLOYMENT_RUNBOOK.md` | No `firebase.json`, `.firebaserc`, frontend or Firebase workflow | Repository inventory | MISSING/BLOCKED | Add minimal hosting config after target project/account is confirmed; no credential guessing. |
| CI/CD | `.github/workflows/ci.yml`, `CI_REQUIREMENTS.md` | install→structure→format→lint→mypy→pytest→build→secret scan | Workflow present | ALIGNED BASELINE | Protect main; add Firebase deploy only after CI and project setup. |

## Material inconsistencies found

1. `CALCULATION_FORMULAS.md` initially said total condenser was prioritized and
   partial could be deferred, while `EXPERT_CONFIRMATION.md` and
   `ALGORITHM_SPEC.md` require both modes in V1. The calculation spec is now
   clarified: total may be implemented first, but partial is still a V1
   deliverable and must stay `NOT_IMPLEMENTED` until its branch/tests exist.
2. The formula document used `0 < zF < 1`, while `PROCESS_MODEL.md` and the
   Pydantic API contract use `[0,1]`. The formula contract now matches the API
   boundary and explicitly guards recovery at zero ethanol feed.
3. The archived logic document contains historical choices (including Wilson,
   alternate heat-loss input and a second system). Current final documents
   explicitly override those choices; archived files must not be used as
   runtime instructions.
4. `EXPERT_CONFIRMATION.md` says the validation metric/threshold was still
   open, while `VALIDATION_ACCEPTANCE.md` later records the accepted value of
   5 percentage points. This is a temporal update, not a scientific conflict;
   the newer acceptance document is authoritative for that one decision.
5. Existing deployment/security wording mentions Firebase but does not state
   the hosting boundary. The runbook now states that Firebase Hosting serves
   static frontend assets only; the Python API needs a separate runtime.

## Calculation closure finding

The original input list can determine a total-condenser solution only after an
outer equation is made explicit. The contract is now:

- unknown: scalar `xD`;
- derived: `B=F-D`, `xB=(F*zF-D*xD)/B`;
- trial construction: rectifying line, q-line, feed intersection and stripping
  line;
- stage solve: exactly `N` body trays, stage `1..NF-1` rectifying and
  `NF..N` stripping;
- bottom closure: equilibrium reboiler boundary
  `r_outer=y_N-y_eq(xB,P)=0`;
- bounds: `xD ∈ [zF, min(1,F*zF/D)]` with endpoint guard;
- numerical method: deterministic finite-grid sign bracket then bisection/Brent;
- acceptance: outer, mass, ethanol and solver residuals `<1e-4` plus physical
  checks.

`NF` is not adjusted. The engine computes `NF_geo` from the geometric feed
transition and returns `INCONSISTENT_FEED_STAGE` when it differs from input
`NF`. Partial condenser is not closed by this formulation and remains an
explicit scientific blocker.

## Documentation closure finding

`UI_UX_SPEC.md` now defines field labels/ranges/defaults, three-column layout,
process diagram, result semantics, stage table, graphs, sensitivity tab and
demo/pending states. `TEST_CASES.md` now lists analytic cases and marks all
numerical values without reviewed sources `PENDING_REFERENCE_REVIEW`.

## Baseline evidence

- Repository structure check: PASS.
- Package build: PASS.
- Direct Ruff/mypy/pytest/detect-secrets executable aliases were not on the
  PowerShell PATH, but the equivalent `python -m ...` checks pass after the
  dev extra was installed.
- Calculation engine, UI, reviewed thermo data, validation and Firebase are
  not complete; these are expected pending work, not false passes.
- Reviewed Antoine data blocks Phase 3/4 scientific output. Enthalpy data blocks
  only Phase 6 energy, not Phase 3/4 VLE/stage implementation.
