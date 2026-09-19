# Algorithm Specification — V1

This is the implementation checklist for the calculation engine. The detailed
equations and closed outer solve are in `PROCESS_MODEL.md` and
`CALCULATION_FORMULAS.md`; this file fixes module order, inputs, outputs and
failure behavior.

## 1. Runtime scope

Use only Raoult + Antoine for V1 runtime. Do not implement Wilson/NRTL, AI/ML,
optimization, dynamic simulation or detailed tray hydraulics. The normal closed
branch is total condenser. Partial condenser remains a separate
`NOT_IMPLEMENTED` branch until its open scientific decisions are approved.

## 2. Deterministic pipeline

1. Validate `SimulationInput`: `F`, `zF`, `q`, `P`, `N`, `NF`, `R`, `D`,
   condenser and absolute `heatLoss_kW`.
2. Load a `REVIEWED` Antoine dataset with component records, units, ranges,
   citation, version, reviewer and review date. A pending dataset cannot
   produce a scientific success.
3. Build Raoult equilibrium functions: Antoine saturation pressure, bubble
   temperature, `y_eq(x,P)` and inverse equilibrium lookup. Attach
   `THERMO_EXTRAPOLATION` with component, actual temperature and source range
   when extrapolation is used.
4. For total condenser, derive `B`, `L`, `V`, `Lbar`, `Vbar`, and solve the
   scalar outer unknown `xD` using the reboiler boundary residual described in
   `PROCESS_MODEL.md`.
5. For each trial, derive `xB`, rectifying line, q-line, feed intersection and
   stripping line. Reject physical violations and singular intersections.
6. Step exactly `N` body stages from the top boundary. Use rectifying line for
   stages `1..NF-1`, stripping line for stages `NF..N`; calculate each stage
   temperature from VLE.
7. Close the equilibrium reboiler boundary without adding the reboiler to `N`.
   Require `NF_geo == NF`; otherwise return `INCONSISTENT_FEED_STAGE` and never
   change the requested `NF`.
8. Compute `D`, `B`, `xD`, `xB`, recovery, stage profile, operating-line data,
   warnings, provenance and residuals.
9. Compute energy only when reviewed enthalpy data is available. Energy is a
   Phase 6 dependency and must not block the Phase 3/4 VLE engine.
10. Return a typed API result. `success` requires every physical gate and all
    residuals strictly `< 1e-4`.

## 3. Outer solver contract

The total-condenser outer solver has one unknown, `xD`; `xB` is derived from
the ethanol balance. Use physical bounds:

```text
xD_low  = zF
xD_high = min(1, F*zF/D)
```

Use a guarded interval, deterministic 101-point scan, first finite sign-change
bracket, then bisection or Brent. The root residual is:

```text
r_outer = y_N - y_eq(xB, P)
```

where `y_N` is the operating-line vapor value after body stage `N`. Record
bracket, iterations, method and final residual. No sign-changing bracket,
failed equilibrium inversion, pinch, NaN/Inf, out-of-range step, iteration
limit or failed physical/residual gate is a success.

## 4. Pure module boundaries

- `thermodynamics`: reviewed data loading, Antoine, bubble point, Raoult and
  equilibrium inversion.
- `distillation`: material balance, operating lines, total-condenser stepping,
  partial-condenser placeholder, stage result and energy boundary.
- `solver`: scalar root/bracket utilities and residual gates.
- `sensitivity`: exactly one of `R`, `N`, `NF`, preserving all other inputs.
- `api`: validation, status/error mapping, provenance and serialization.
- `ui`: rendering only; it must not recalculate science.

The energy function must remain pure and tested:
`calcEnergy(input, solution, enthalpyData)`. It uses cited Cp/latent heat and
the fixed sign convention; it is not a second VLE model.

## 5. Output minimum

The engine/API returns:

```text
status
errorCode (nullable)
D_kmol_h
B_kmol_h
xD
xB
recovery_ethanol_percent
QC_kW / QR_kW / heatLoss_kW (nullable until Phase 6)
residuals.totalMass
residuals.ethanolBalance
residuals.solver
thermoModel = "raoult-antoine"
thermoDataVersion
isExtrapolated
warnings[]
stages[]
operatingLines
trace[]
```

`stages[]` contains `stage`, `T_C`, `x_ethanol`, `y_ethanol` and
`section=rectifying|stripping`. Feed transition metadata contains `NF`,
`NF_geo`, `xq`, `yq` and any consistency error.

## 6. Status/error behavior

- Invalid payload: HTTP/API validation error with `INVALID_INPUT` semantics.
- Valid total-condenser input before engine/data readiness: explicit pending or
  failed response; never fake scientific values.
- Valid partial-condenser input while contract is open: `not_implemented` and
  `NOT_IMPLEMENTED`.
- Extrapolated but physical success: success/warning result with persistent
  warning metadata; warnings cannot be hidden by a success badge.
- Any residual or physical failure: non-success status with trace and reason.
