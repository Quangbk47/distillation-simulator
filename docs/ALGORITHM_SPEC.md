# Algorithm Specification Final

1. Validate input, bao gồm `heatLoss_kW` và direct q.
2. Load reviewed Antoine data, create VLE by Raoult; append extrapolation warning when needed.
3. Create diagonal, rectifying line, q-line, stripping line.
4. Apply McCabe-Thiele using body-stage convention; support explicit total/partial-condenser branch.
5. Compute D/B/compositions/recovery; reject physical violations.
6. Compute QC/QR with simple enthalpy model and absolute heat loss in kW; return component contributions for audit.
7. Compute total-mass, ethanol-component and solver residuals. Success only if all are <1e-4.
8. Return result, warnings, trace and data provenance.

Energy function must be pure and tested: `calcEnergy(input, solution, enthalpyData)`. Do not implement Wilson in the run path.
