# CI Requirements

Every pull request and push to `main` runs:

```text
install
→ repository structure
→ format check
→ lint
→ type check
→ unit/integration/reference/validation tests
→ production package build
→ secret scan
```

`main` requires reviewer approval and green checks before merge. A scientific
model/data change also requires scientific-lead review, provenance update and
appropriate regression/reference tests. A pending reference case must remain
pending; CI must not be changed to make it appear PASS.

Firebase deployment is a later gate: frontend deploy runs only after CI passes,
and production deploy is blocked when any check fails. The Python backend is
deployed separately from Firebase Hosting.
