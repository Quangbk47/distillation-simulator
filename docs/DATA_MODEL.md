# Data Model — V1 API contract

The backend is the calculation authority. The browser sends input and renders
typed output; it never owns authoritative thermo data or recomputes results.

## 1. Simulation input

The current wire model is `SimulationInput` in `src/api/schemas.py`:

```json
{
  "F_kmol_h": 100.0,
  "zF_ethanol": 0.5,
  "q": 1.0,
  "P_bar": 1.01325,
  "N": 10,
  "NF": 5,
  "R": 2.0,
  "D_kmol_h": 20.0,
  "heatLoss_kW": 0.0,
  "condenser": "total"
}
```

`extra=forbid` is required. Constraints are:

- `F_kmol_h > 0`;
- `0 < zF_ethanol < 1` for a normal column solve;
- `q` is finite and direct;
- `P_bar > 0`;
- `N` integer `>= 1`, `NF` integer `1..N`;
- `R >= 0`;
- `0 < D_kmol_h < F_kmol_h`;
- `heatLoss_kW >= 0` and is an absolute kW load;
- `condenser` is exactly `total` or `partial`.

Pure-component `x=0`/`x=1` limits remain thermo-unit tests, not a normal
simulation input. No efficiency, `Tfeed`, reboiler selector, alternate model
or hidden input is allowed in the minimum UI/API.

## 2. Simulation result

The result must preserve these fields even when values are pending or failed:

```json
{
  "status": "not_implemented",
  "errorCode": null,
  "D_kmol_h": null,
  "B_kmol_h": null,
  "xD": null,
  "xB": null,
  "recovery_ethanol_percent": null,
  "thermoModel": "raoult-antoine",
  "thermoDataVersion": "reviewed-version",
  "isExtrapolated": false,
  "warnings": [],
  "residuals": {
    "totalMass": null,
    "ethanolBalance": null,
    "solver": null,
    "outer": null
  },
  "QC_kW": null,
  "QR_kW": null,
  "heatLoss_kW": 0.0,
  "energyBreakdown": null,
  "operatingLines": null,
  "stages": [],
  "trace": []
}
```

This is a pending-result shape example only, not a scientific golden case. A
`success` result must populate the calculation fields after the engine and
reviewed data are ready. Do not copy placeholder values into tests.

`success` requires total-mass, ethanol-balance, outer/root and solver residuals
strictly below `1e-4`, plus all physical checks. `warning` means a physical
success with visible warning(s), especially `THERMO_EXTRAPOLATION`.

## 3. Stage record

Every body tray record contains:

```json
{
  "stage": 1,
  "T_C": 78.0,
  "x_ethanol": 0.80,
  "y_ethanol": 0.88,
  "section": "rectifying|stripping"
}
```

`stage=1` is the top body tray and `stage=N` is the bottom body tray. The
condenser and equilibrium reboiler boundary are not emitted as body-stage
numbers. Stage temperature is calculated from bubble-point VLE.

## 4. Feed/solver metadata

The result trace/operating-line metadata may expose:

- `NF` requested by the user;
- `xq`, `yq` feed intersection for operating-line visualization;
- `xD` search bounds, bracket, numerical method and iterations;
- final outer residual;
- warnings and data provenance.

The feed intersection is diagnostic only. Never rewrite the user's `NF` and do
not fail a case merely because the geometric crossing lies between stages.

## 5. Partial condenser status

Partial condenser remains in the enum because it is a V1 deliverable, but its
scientific formulation is OPEN/BLOCKING in `PROCESS_MODEL.md`. Until approved:

```json
{
  "status": "not_implemented",
  "errorCode": "NOT_IMPLEMENTED",
  "warnings": ["PARTIAL_CONDENSER_CONTRACT_OPEN"]
}
```

No `xD`, `xB`, duty or stage values may be presented as calculated for this
branch. The API may use HTTP 501 for this explicit capability state, with the
typed error payload documented by the implementation.

## 6. Thermodynamic provenance

`thermoDataVersion` identifies a reviewed data file. Every Antoine record must
carry component, `A/B/C`, formula, pressure unit, temperature range/unit,
citation, publication/version, reviewer and review date. Extrapolation stores
the component, actual temperature and source range in warning/trace metadata.

## 7. Sensitivity request/result

`SensitivityRequest` contains one `base` simulation input, one parameter from
`R|N|NF`, and a non-empty values list. Each run changes exactly that parameter;
q, condenser, heat loss and all other inputs remain fixed. The result is a
series of typed simulation summaries, not an optimizer output.

## 8. Validation data

`ValidationCase` stores case ID, source citation/type, source conditions, input
mapping, observed values/units and `validationAcceptance`. The accepted metric
is `MAE_xD_xB_percentage_points` with threshold `5`; `value`/`pass` remain null
until the source and mapping are reviewed and the case is evaluated.
