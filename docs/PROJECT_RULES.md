# Project Rules Final

Use only Raoult + Antoine in V1 runtime. q is a direct user input; heat loss is absolute kW. Support total and partial condenser; N is body stages only. Extrapolation is allowed only with structured warning/provenance. A solver success requires all balance and solver residuals <1e-4. Backend/API is production authority; no secret or authoritative data in client. Validation V1 uses MAE of xD/xB in percentage points with an accepted threshold of 5; see `VALIDATION_ACCEPTANCE.md`.
