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

The technical team opens/reviews PRs and merges to `main` after the required
review and green checks; Owner approval is not a technical gate. A scientific
model/data change additionally requires the designated scientific-lead/expert
decision, provenance update and appropriate regression/reference tests. A
pending reference case must remain pending; CI must not be changed to make it
appear PASS.

After merge, build the production artifact and deploy Firebase Hosting using a
student-controlled Firebase account/project/site when necessary. The frontend
deploy runs only after the merged commit has passed CI, and deployment must
stop when any check fails. The Python backend is deployed separately from
Firebase Hosting. A release passes only after the public production URL is
reachable, the production smoke test passes, and evidence is updated.
