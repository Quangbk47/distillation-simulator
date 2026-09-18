# Test Cases Final

Required tests:
- q direct input valid/invalid; heatLoss_kW 0/positive/negative.
- N counts body stages only.
- Total condenser and partial condenser reference cases.
- Antoine in range, extrapolated warning, and reject nonphysical extrapolation.
- Raoult + Antoine metadata always returned; Wilson unavailable through runtime API.
- Energy unit tests with cited Cp/latent-heat fixture and absolute heat-loss kW.
- total mass, component, solver residual individually below 1e-4; any one failure returns non-success.
- API authorization, schema validation, data-version provenance, stale-result prevention.
- Literature validation cases store citation and condition mapping.
