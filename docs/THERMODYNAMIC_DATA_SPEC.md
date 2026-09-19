# Thermodynamic Data Specification

## Runtime role

V1 runtime has exactly one VLE model: Raoult + Antoine for Ethanol–Water.
Antoine data review blocks scientific Phase 3/4 output. Enthalpy data review
does **not** block Phase 3/4; it blocks only Phase 6 energy fields.

## Required record

Each component record in `data/thermodynamics/` must contain:

- component name (`ethanol` or `water`);
- Antoine `A`, `B`, `C` and the exact formula;
- coefficient temperature unit and valid temperature range;
- saturation-pressure unit and conversion to `P_bar`;
- source citation/URL, publication/version;
- reviewer and review date;
- dataset/schema version.

The two component records must use a compatible formula/unit convention. Do not
mix coefficients from different pressure or temperature units.

## Runtime rules

- Only `status=REVIEWED` data can produce a scientific success.
- `PENDING_REVIEW` is a repository placeholder, not a fallback dataset.
- Outside the reviewed temperature range, physical extrapolation may continue
  with `THERMO_EXTRAPOLATION`, actual temperature and source range in result
  metadata.
- Reject non-positive/NaN/Inf saturation pressure, impossible equilibrium or
  missing provenance; never silently clamp.
- Wilson/NRTL records may be discussed as future work but are not exposed by
  V1 API/UI.

## Enthalpy data

Phase 6 separately reviews Cp, latent heat, reference temperature, units and
source. These records must have the same provenance fields and a version. Until
reviewed, QC/QR are `null`/pending and the UI says `NOT CALCULATED`; no duties
are fabricated to make the demo look complete.
