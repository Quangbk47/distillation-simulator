# Software Architecture — V1

## 1. Boundary

```text
browser UI → backend/API → calculation engine → reviewed data repository
                                      ↓
                                  typed result
```

The backend is the only calculation authority. Firebase Hosting may serve the
static browser client, but it does not run the Python API. The API therefore
needs a separate small runtime; do not introduce microservices, Kubernetes or
a database unless a later decision explicitly requires it.

## 2. Repository responsibilities

| Area | Responsibility | Must not do |
|---|---|---|
| `src/thermodynamics` | Load reviewed records, Antoine, Raoult, bubble point, equilibrium inversion | Store unreviewed constants or Wilson/NRTL runtime logic |
| `src/distillation` | Flows/balances, operating lines, closed total-condenser solver, partial placeholder, stage records, energy boundary | Read UI state or invent result values |
| `src/solver` | Bracket/root utilities, iteration trace and residual gates | Hide failed convergence |
| `src/sensitivity` | One-variable R/N/NF sweeps | Optimize or vary multiple variables |
| `src/api` | Pydantic validation, engine dispatch, status/error/provenance serialization | Become a second calculation implementation |
| `src/ui` | Render inputs, process diagram, tables and graphs from API result | Recalculate science or own thermo data |
| `data/thermodynamics` | Reviewed Antoine data and provenance | Accept `PENDING_REVIEW` as runtime data |
| `data/validation` | Reviewed reference cases and acceptance evidence | Claim PASS without review/evaluation |
| `tests` | Unit, integration, reference, validation and smoke contracts | Use fake scientific values as golden evidence |

## 3. Request flow

1. UI validates basic form shape and sends `SimulationInput`.
2. API validates all constraints again with `extra=forbid`.
3. API rejects/marks partial as `NOT_IMPLEMENTED` while the contract is open.
4. Engine loads reviewed data and runs the deterministic total-condenser
   pipeline/outer solve.
5. Engine returns values, stage table, operating-line data, warnings, trace,
   provenance and residuals.
6. API maps the typed result to JSON and records request/data/commit metadata
   without logging secrets.
7. UI renders the response; stale results are cleared when a new request starts
   or fails.

## 4. API surface

- `GET /health`: process health only; does not claim scientific readiness.
- `GET /api/thermo-data/version`: model and reviewed/pending data version.
- `POST /api/simulations`: typed input to typed result/error.
- `POST /api/sensitivity`: one-variable sweep after the engine is ready.
- Validation/admin endpoints are deferred until authentication/authorization
  and backend runtime are explicitly selected.

The API returns no scientific success when reviewed thermo data is absent. A
partial-condenser request returns explicit `not_implemented`/`NOT_IMPLEMENTED`
until the scientific contract is approved.

## 5. Configuration and security

- `.env.example` documents non-secret local settings.
- Secrets, service credentials and authoritative data stay server-side.
- CORS/allowed origins and auth are backend deployment concerns.
- CI runs structure, format, lint, type-check, tests, build and secret scan.
- Firebase Hosting deploys only the frontend artifact; backend deployment is a
  separate release with compatible API/data versions.

## 6. Minimal implementation sequence

1. Keep current package/CI skeleton green.
2. Add static UI shell and early Firebase Hosting connection.
3. Implement reviewed thermo/material functions.
4. Implement total-condenser closure and stage solver.
5. Integrate API/UI and deploy the vertical slice.
6. Add energy, sensitivity, validation and hardening in roadmap order.
