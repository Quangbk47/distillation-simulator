# Test Cases — V1

## 1. Test policy

Tests are grouped as unit, integration, reference and validation tests. A
scientific expected number is allowed only when the source, units, model,
conditions and reviewer are recorded. Otherwise the case is explicitly
`PENDING_REFERENCE_REVIEW`; it is not a PASS and must not be filled with a
plausible invented value.

All successful simulation cases require:

```text
totalMass < 1e-4
ethanolBalance < 1e-4
outer < 1e-4
solver < 1e-4
```

## 2. Contract/unit cases

| ID | Case | Expected behavior | Status |
|---|---|---|---|
| C-01 | Valid direct q and zero heat loss | Payload accepted; q preserved; heat loss is `0` | Implemented contract |
| C-02 | Positive absolute heat loss | Payload accepted in kW, not percent | Implemented contract |
| C-03 | `F <= 0`, `P <= 0` | Reject `INVALID_INPUT` | Required |
| C-04 | `zF <= 0` or `zF >= 1` in simulation | Reject normal-column input; pure limits tested only in VLE | Required |
| C-05 | `D <= 0` or `D >= F` | Reject because `B`/`R=L/D` are not valid | Required |
| C-06 | `N < 1`, non-integer N, `NF < 1`, `NF > N` | Reject; do not clamp | Partly implemented |
| C-07 | Negative heat loss | Reject | Required |
| C-08 | NaN/Inf q or numeric field | Reject | Required |
| C-09 | Extra/unknown payload key | Reject due to `extra=forbid` | Implemented contract |

## 3. Thermodynamic cases

| ID | Case | Expected behavior | Expected numerical data |
|---|---|---|---|
| T-01 | Antoine in source range | Positive Psat with provenance and no extrapolation warning | Pending reviewed Antoine dataset |
| T-02 | Antoine outside source range | Physical result plus `THERMO_EXTRAPOLATION`, actual T and source range | Pending reviewed dataset/range |
| T-03 | Non-positive/NaN Psat or invalid denominator | Reject calculation | Analytic expectation; implement unit test |
| T-04 | Pure water `x=0` | Finite bubble point/equilibrium endpoint | Expected numeric value pending source review |
| T-05 | Pure ethanol `x=1` | Finite bubble point/equilibrium endpoint | Expected numeric value pending source review |
| T-06 | Representative Ethanol–Water bubble point | `bubble_temperature(x,P)` and `equilibrium_y(x,P)` are finite and consistent | `PENDING_REFERENCE_REVIEW` |

## 4. Operating-line and closure cases

| ID | Case | Expected behavior | Expected numerical data |
|---|---|---|---|
| O-01 | q=1 | Vertical q-line `x=zF`; no division by zero | Analytic expected structure |
| O-02 | q≠1 | q-line uses `q/(q-1)` formula | Analytic expected structure |
| O-03 | Rectifying line | `mR=R/(R+1)`, `bR=xD/(R+1)` for a trial xD | Analytic expected structure |
| O-04 | Stripping line | Passes through `(xB,xB)` and `(xq,yq)`; singular case rejected | Analytic expected structure |
| O-05 | Outer closure | Scan physical xD bounds, bracket, root-solve `yN-y_eq(xB,P)` | Numeric value pending thermo/reference review |
| O-06 | Valid NF | `NF_geo == NF`, sections are `1..NF-1` rectifying and `NF..N` stripping | Analytic expected structure |
| O-07 | Inconsistent NF | Return `INCONSISTENT_FEED_STAGE`; never change NF | Required |
| O-08 | No xD sign-changing bracket | Return `ROOT_BRACKET_NOT_FOUND`/`NON_CONVERGED` | Required |
| O-09 | Pinch, out-of-range, NaN/Inf, iteration limit | Non-success with trace and reason | Required |

## 5. Condenser cases

| ID | Case | Expected behavior | Status |
|---|---|---|---|
| K-01 | Total condenser | `y_top=xD`, `L=R*D`, `V=(R+1)*D`; condenser/reboiler excluded from N | Contract closed; reference pending |
| K-02 | Total condenser end-to-end | N body stages plus equilibrium reboiler boundary close all residuals | `PENDING_REFERENCE_REVIEW` |
| K-03 | Partial condenser before approval | `status=not_implemented`, `errorCode=NOT_IMPLEMENTED`, no scientific values | Explicitly blocked |
| K-04 | Partial condenser after approval | Independent phase/product/equilibrium/stage-count equations and golden case | Contract decision required |

## 6. Material/recovery cases

| ID | Case | Expected behavior | Expected numerical data |
|---|---|---|---|
| M-01 | Material balance identity | `F=D+B` and normalized residual `<1e-4` | Analytic |
| M-02 | Ethanol balance identity | `F*zF=D*xD+B*xB` and normalized residual `<1e-4` | Analytic |
| M-03 | Recovery | `100*D*xD/(F*zF)`, never `D/F` | Analytic |
| M-04 | Physical composition ordering | Reject if `0<=xB<=zF<=xD<=1` fails | Analytic |

The old illustrative balance example in `CALCULATION_FORMULAS.md` is a formula
check only, not an end-to-end golden simulation case.

## 7. Energy cases

| ID | Case | Expected behavior | Status |
|---|---|---|---|
| E-01 | Energy sign convention | Typical `QC < 0`, `QR > 0` under approved fixture | `PENDING_REFERENCE_REVIEW` |
| E-02 | Heat-loss delta | Increasing `heatLoss_kW` increases QR by the documented energy amount | Fixture/source pending |
| E-03 | Unit conversion | kmol/h × kJ/kmol / 3600 = kW | Analytic; fixture pending |
| E-04 | Missing/unreviewed enthalpy data | Phase 3/4 remains runnable; Phase 6 energy is pending, not fake | Required |

## 8. API/UI cases

| ID | Case | Expected behavior |
|---|---|---|
| A-01 | Health/version endpoints | Report process/data readiness without claiming simulation readiness |
| A-02 | Invalid payload | Typed validation error; no stale result |
| A-03 | Pending total branch | Explicit pending/failed state; no fake values |
| A-04 | Partial request | Explicit `NOT_IMPLEMENTED` state |
| A-05 | Extrapolation warning | Persistent UI warning names component, temperature and source range |
| A-06 | Stage table/graph | Render returned data only; no frontend recalculation |
| A-07 | Sensitivity | Only R, N or NF changes; q/condenser/heatLoss remain fixed |

## 9. Acceptance rule

Do not call the engine, UI, validation or deployment complete because a schema
or placeholder test passes. Promote a case from `PENDING_REFERENCE_REVIEW` only
after source citation, condition mapping, units, observed/expected data,
reviewer and review date are recorded.
