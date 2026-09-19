# UI boundary

The complete UI contract is [`docs/UI_UX_SPEC.md`](../../docs/UI_UX_SPEC.md).
This directory is a thin client of the backend API:

- render the LEFT input / CENTER process visualization / RIGHT results layout;
- expose direct q, absolute `heatLoss_kW`, `N`, `NF`, `R`, `D_kmol_h` and
  condenser selection;
- render xD/xB as ethanol mole fractions, stage table, temperature graph,
  warnings, provenance and all residuals;
- show `DEMO`, `NOT CALCULATED` or `ENGINE NOT CONNECTED` before the engine is
  ready;
- never own authoritative thermo data or duplicate scientific calculations.
