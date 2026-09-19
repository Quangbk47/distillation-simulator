# Process Model — V1 calculation contract

This document defines the problem that the engine must solve. It is more
specific than the project scope and is the canonical bridge between the
scientific decisions and `CALCULATION_FORMULAS.md`/`ALGORITHM_SPEC.md`.

## 1. Scope and conventions

- System: binary Ethanol–Water; ethanol is the light component.
- Model: steady-state, constant pressure, Raoult + Antoine VLE.
- Method: McCabe–Thiele with constant molar overflow.
- `N`: theoretical body trays only. The condenser and reboiler are never
  included in `N`.
- `NF`: feed tray counted from the top body tray, `1 <= NF <= N`.
- `q`: direct numeric feed thermal condition; it is not inferred from `Tfeed`.
- `D` is the specified distillate flow. `B`, `xD` and `xB` are solved/derived.
- A normal simulation requires `0 < zF < 1` and `0 < D < F`; pure-component
  limits belong to VLE tests, not the normal column solve.

The total-condenser formulation below is CLOSED for implementation. The partial
condenser formulation is intentionally OPEN/BLOCKING; see Section 9.

## 2. Input contract

| API field | Symbol | Type/unit | Constraint |
|---|---|---|---|
| `F_kmol_h` | `F` | number, kmol/h | `F > 0` |
| `zF_ethanol` | `zF` | number, mol/mol | `0 < zF < 1` |
| `q` | `q` | finite number, dimensionless | direct input; no fixed artificial range |
| `P_bar` | `P` | number, bar | `P > 0`; convert consistently with Antoine pressure unit |
| `N` | `N` | integer, body trays | `N >= 1` |
| `NF` | `NF` | integer, body-tray index | `1 <= NF <= N` |
| `R` | `R=L/D` | number, dimensionless | `R >= 0` |
| `D_kmol_h` | `D` | number, kmol/h | `0 < D < F` |
| `condenser` | — | enum | `total` or `partial` |
| `heatLoss_kW` | `Qloss` | number, kW | `Qloss >= 0`; absolute load |

The UI may display `D_kmol_h`; the calculation symbol remains `D`. No tray
efficiency, reboiler selector, alternate thermo model or `Tfeed` input is part
of the minimum V1 input contract.

## 3. Derived flows and balances

For every trial/solution:

```text
B = F - D
L = R*D
V = L + D = (R+1)*D
Lbar = L + q*F
Vbar = V - (1-q)*F
F = D + B
F*zF = D*xD + B*xB
xB = (F*zF - D*xD)/B
Recovery_E = D*xD/(F*zF)
```

The normal separation physical check is:

```text
0 <= xB <= zF <= xD <= 1
```

The solver must reject a trial that violates this check, produces a
non-positive flow, or produces NaN/Inf. It must not silently clamp a value.

## 4. Calculation closure: total condenser

### 4.1 Unknown and governing equations

For the closed total-condenser branch, the only outer unknown is:

```text
xD = ethanol mole fraction in the distillate
```

`xB` is derived from the ethanol balance above. For a trial `xD`, construct:

```text
mR = R/(R+1)
bR = xD/(R+1)
yR(x) = mR*x + bR
```

For `q != 1`, the q-line is:

```text
yqline(x) = q/(q-1)*x - zF/(q-1)
```

For `q = 1`, use the vertical line `x = zF`; never divide by `q-1`.
The intersection `(xq,yq)` is the intersection of the rectifying line and
q-line. The stripping line is the line through `(xB,xB)` and `(xq,yq)`.

The stage stepping produces `y_N`, the vapor composition after the last body
tray. The equilibrium reboiler boundary is:

```text
y_N = y_eq(xB, P)
```

Therefore the scalar outer root residual is:

```text
r_outer(xD) = y_N(xD) - y_eq(xB(xD), P)
```

The outer root is accepted only when `abs(r_outer) < 1e-4`, all physical checks
pass, and the total/component residuals are also below `1e-4`.

This convention treats the reboiler as an equilibrium boundary stage for the
bottom equation, but it does not count that reboiler in `N`.

### 4.2 Physical bounds and bracket

For `D > 0`, normal ethanol-to-distillate separation gives:

```text
xD_low  = zF
xD_high = min(1, F*zF/D)
```

The numerical search interval is the open physical interval between these
bounds, with a small endpoint guard `epsilon = 1e-12` or the implementation's
documented equivalent. If `xD_high <= xD_low`, return a physical input/solve
error; do not run a degenerate root search.

The engine samples a deterministic 101-point grid over the guarded interval,
keeps finite trial residuals, and selects the first adjacent sign-changing
bracket. If no sign-changing bracket exists, return `NON_CONVERGED` with
`ROOT_BRACKET_NOT_FOUND`; do not return the trial with the smallest residual as
if it were a solution.

### 4.3 Numerical method and stopping rules

Use bisection or Brent on the selected scalar bracket. The implementation must
record the method, bracket, iteration count and final `r_outer` in `trace`.
Stop when either:

- `abs(r_outer) < 1e-4`, or
- the bracket width is below the documented numerical floor.

The second condition is not sufficient by itself: the residual gate must still
pass. Return `NON_CONVERGED` for NaN/Inf, failed equilibrium inversion, pinch,
out-of-range stepping, iteration limit or failed residual/physical gates.

## 5. Stage indexing and boundaries

Stages are counted from top to bottom:

```text
stage 1 = top body tray directly below the condenser
stage NF = feed tray
stage N = bottom body tray directly above the reboiler
```

### Top boundary — total condenser

The total condenser is not an equilibrium stage in the body-stage count:

```text
y_top = xD
x_reflux = x_distillate = xD
L = R*D
V = (R+1)*D
```

Stepping starts at `(xD, xD)`: horizontally to the equilibrium curve for
stage 1, then vertically to the selected operating line.

### Body-stage transition

For the input `NF`:

```text
stages 1 .. NF-1 : rectifying line
stages NF .. N   : stripping line
```

The feed tray itself is therefore the first stripping-section body tray. Each
stage stores `stage`, `section`, `x_ethanol`, `y_ethanol` and `T_C`.

### Bottom boundary — equilibrium reboiler

After stage `N`, the current operating-line vapor value is `y_N`. The reboiler
liquid has composition `xB` and its equilibrium vapor is `y_eq(xB,P)`. The
outer residual in Section 4 closes these values. The reboiler is not included
in the returned body-stage count.

## 6. NF/feed-stage consistency

`NF` is a hard input, never an output to be silently adjusted.

For every trial, the engine also computes the geometric feed transition using
the same q-line intersection. Define `NF_geo` as the first body-stage index
whose equilibrium horizontal step reaches the stripping side of the feed
intersection (`x_i <= xq` using the implementation's documented tolerance).
If no such step occurs in `1..N`, use `NF_geo = N+1`.

The result is valid only when `NF_geo == NF`. Otherwise return:

```text
status = "failed"
errorCode = "INCONSISTENT_FEED_STAGE"
```

The engine must include `NF`, `NF_geo`, `xq`, `yq` and the tolerance in the
trace. It must not move the feed, change `NF`, or substitute another operating
line to force a match. A root failure before this check remains
`NON_CONVERGED`, not `INCONSISTENT_FEED_STAGE`.

## 7. Total-condenser stepping algorithm

```text
validate input and reviewed thermo data
compute B, L, V, Lbar, Vbar
trial xD within physical bounds
derive xB from ethanol balance
build rectifying line and q-line intersection
build stripping line through (xB, xB) and (xq, yq)
current_y = xD
for i in 1..N:
    x_i, T_i = equilibrium_inverse(current_y, P)
    section = rectifying if i < NF else stripping
    current_y = line(section, x_i)
    store stage i
r_outer = current_y - equilibrium_y(xB, P)
root-solve r_outer(xD) = 0
check NF_geo == NF, balances, physical bounds and all residual gates
return typed result, trace, warnings and provenance
```

The implementation may factor this into pure functions, but must preserve the
same observable convention and trace information.

## 8. Failure/status contract

- `success`: all residuals are strictly `< 1e-4`, physical checks pass and
  required reviewed data exists.
- `warning`: only when the calculation succeeds but a structured warning such
  as `THERMO_EXTRAPOLATION` is present; success must not hide the warning.
- `failed`: invalid physical input, inconsistent NF, non-convergence or failed
  residual gate.
- `not_implemented`: a valid partial-condenser request while the partial
  contract is still OPEN/BLOCKING.

Required error codes include `INVALID_INPUT`, `ROOT_BRACKET_NOT_FOUND`,
`NON_CONVERGED`, `INCONSISTENT_FEED_STAGE`, `THERMO_EXTRAPOLATION` and
`NOT_IMPLEMENTED`.

## 9. Partial condenser — OPEN/BLOCKING contract

The current expert decisions require partial condenser support in V1 but do not
uniquely specify the physical formulation. The repository must not invent one.
Until the questions below are answered and recorded by the scientific lead,
the partial branch returns `status="not_implemented"` and
`errorCode="NOT_IMPLEMENTED"` without scientific numbers.

The following decisions are blocking:

1. Product convention: is `D` the liquid distillate, vapor distillate, or a
   split with both phases? Is reflux liquid, vapor, or phase-split?
2. Equilibrium relation: should the partial condenser be one equilibrium stage
   using Raoult + Antoine at condenser pressure, and is pressure equal to `P`?
3. Stage count: does the partial condenser count as an equilibrium stage in
   addition to the `N` body trays, while the reboiler remains outside `N`?
4. Flow equations: what are `L`, `V`, distillate phase flow and reflux flow
   under the chosen product convention?
5. Boundary/unknowns: which condenser temperature, vapor/liquid composition
   and phase fraction are unknown, and what equations close them?
6. Residual: which condenser equilibrium and total/component balances are
   required, and how are they combined with the outer xD/root residual?
7. Reference case: which reviewed input/output case is the golden test?

After approval, update this section, `ALGORITHM_SPEC.md`, `DATA_MODEL.md`,
API status semantics, tests and the Phase 4 Definition of Done before enabling
partial values.

## 10. Energy boundary

Energy is not required to close Phase 3/4 VLE and stage calculations. Phase 6
uses the reviewed Cp/latent-heat data and the fixed convention:

```text
QC < 0  (heat removed)
QR > 0  (heat supplied)
F*hF + QR + QC = D*hD + B*hB + Qloss
```

`Qloss` is an absolute non-negative kW load. Increasing it must increase the
required `QR` by the same energy amount under the chosen convention.
