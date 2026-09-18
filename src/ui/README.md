# UI boundary

The production UI will be a thin client of the backend API. It must expose direct `q`, absolute `heatLoss_kW`, total/partial condenser selection, warnings and all residuals. No authoritative thermodynamic data or calculation logic belongs in this directory.
