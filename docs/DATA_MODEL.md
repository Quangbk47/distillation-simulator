# Data Model Final

SimulationInput adds `heatLoss_kW:number` (not fraction), direct `q:number`, and `condenser:'total'|'partial'`.

SimulationResult metadata: `thermoModel:'raoult-antoine'`, `thermoDataVersion`, `isExtrapolated`, `warnings[]`. Energy: `QC_kW`, `QR_kW`, `heatLoss_kW`, `energyBreakdown`. Residuals: `totalMass`, `ethanolBalance`, `solver`; `status:'success'` only when all <1e-4.

ValidationCase requires `sourceCitation`, `sourceType:'experimental'|'literature'`, `sourceConditions`, observed values and units. `validationAcceptance` stores metric/threshold/value/pass; V1 uses `MAE_xD_xB_percentage_points` with threshold `5`, while value/pass remain unset until a reviewed case is evaluated.
