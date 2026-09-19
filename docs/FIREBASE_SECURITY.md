# Firebase Security

The production architecture requires a backend/API. Firebase Hosting, if
selected, serves the static frontend only; it does not expose or execute the
Python calculation authority. A separate backend runtime owns authenticated
calculation, reviewed thermo data and validation records.

The client may read public demo cases, but direct client writes to component
constants and validation evidence are denied. Server/service-account writes,
if eventually needed, remain backend-only. Secrets and service credentials are
never committed. Test hosting rules, API authorization and allowed origins in
CI/staging before production.
