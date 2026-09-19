# Project Scope

## V1 objective

Build a small teaching/research simulator for a binary Ethanol–Water column:

```text
input → backend calculation engine → numbers + column diagram + stage table + graphs
```

V1 is steady-state, constant-pressure and uses Raoult + Antoine VLE with
McCabe–Thiele. The closed total-condenser calculation contract is defined in
[`PROCESS_MODEL.md`](PROCESS_MODEL.md) and
[`CALCULATION_FORMULAS.md`](CALCULATION_FORMULAS.md). Partial condenser remains
a V1 deliverable but is OPEN/BLOCKING until its missing physical conventions
are approved; it must return `NOT_IMPLEMENTED` before then.

V1 includes direct numeric q, body-stage `N`/`NF`, material/component balance,
ethanol recovery, simple QC/QR energy, absolute `heatLoss_kW`, sensitivity of
one variable at a time (`R`, `N` or `NF`), scientific validation and a simple
web UI.

## Explicitly out of scope

Do not add a second chemical system, Wilson/NRTL runtime, optimization, AI/ML,
dynamic simulation, detailed tray hydraulics, 3D animation, enterprise
dashboard, microservices, Kubernetes, complex database or user-selectable
thermodynamic models in V1.

## Later milestone

A second system and operating-region recommendation may be considered only
after a new scientific decision. Do not choose that system in code or roadmap
tasks now.
