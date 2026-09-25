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

`main` requires a completed PR review and green checks before merge. This is a
review gate on the change, not a requirement to wait for a separate Owner
approval at every Phase. A scientific model/data change also requires the
designated scientific-lead review, provenance update and appropriate
regression/reference tests. A pending reference case must remain pending; CI
must not be changed to make it appear PASS.

Firebase deployment follows merge: frontend deploy runs only after the merged
commit has passed CI, and production deploy is blocked when any check fails.
The Python backend is deployed separately from Firebase Hosting. The production
smoke test and evidence update are part of the same release workflow.
