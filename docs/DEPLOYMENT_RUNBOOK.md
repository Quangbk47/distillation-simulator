# Deployment Runbook Final

Deploy backend and frontend separately. Backend environment includes reviewed thermo-data version, validation store credentials, monitoring and allowed origins. Release gate: all total/partial condenser tests, energy tests, residual tests, API auth tests and extrapolation-warning smoke test pass.

Production smoke test: normal in-range case, extrapolated case, total condenser, partial condenser, invalid q, negative heat loss, non-convergent case, unauthorized API request. Roll back both API artifact and data version together when scientific defect occurs.
