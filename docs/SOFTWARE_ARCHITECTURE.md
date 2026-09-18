# Software Architecture Final

Web client → authenticated backend API → calculation engine/data repository. Browser never owns authoritative thermo data or validation records. Backend exposes `POST /api/simulations`, `POST /api/sensitivity`, `GET /api/thermo-data/version`, and protected validation endpoints.

API validates payload, executes deterministic engine, writes audit metadata (case id, commit/data version, warnings/residuals), and returns typed result. Engine modules: `antoine-raoult`, `mccabe-thiele`, `condenser`, `energy`, `convergence`. Both condenser modes are unit/integration tested. Use CI-protected main and environment secrets only server-side.
