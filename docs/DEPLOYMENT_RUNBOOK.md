# Deployment Runbook

## Architecture boundary

Deploy the frontend and backend separately:

- Firebase Hosting may serve the static frontend, preview/staging assets and
  public build metadata.
- Firebase Hosting does not run the Python/FastAPI calculation authority.
- The backend/API needs a separate approved runtime, with server-side secrets,
  reviewed thermo-data version, validation-store access, monitoring and
  allowed origins.

Do not create a Firebase project or process credentials without the owner
confirming the target project/account. Never commit tokens, passwords, service
account private keys or API secrets.

## Early and iterative deployment

1. Phase 1: verify local build and status page.
2. Phase 2: confirm Firebase target, add `firebase.json`/`.firebaserc` and
   manually deploy the minimum static status page. Record URL, project ID and
   commit only after owner login/confirmation.
3. Phase 5: deploy the minimum functional UI after CI passes. Use preview or
   staging if available; keep the backend URL in environment configuration.
4. Phase 9: repeat deployment for hardening smoke tests.
5. Phase 10: production frontend plus separately deployed backend/API.

Automatic production deployment is optional until branch protection, secrets,
runtime ownership and CI gates are confirmed. Never deploy production when
tests fail.

## Release gate

All structure, format, lint, type-check, unit, integration, reference,
validation, build and secret-scan checks must pass. The release must also have
total/partial condenser tests, energy tests, residual tests, API auth tests and
the extrapolation-warning smoke test.

## Production smoke test

Run and record: normal in-range case, extrapolated case, total condenser,
partial condenser, q=1, invalid q, negative heat loss, non-convergent case,
unauthorized API request, energy case and each sensitivity sweep.

Record production URL(s), Firebase project ID, API runtime, commit SHA,
release/version and deployment date. Roll back frontend, API artifact and
scientific data version together when a scientific defect is found.
