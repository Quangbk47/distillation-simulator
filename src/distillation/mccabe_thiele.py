"""Minimum V1 Raoult-Antoine and total-condenser McCabe-Thiele engine."""

import json
from bisect import bisect_left
from collections.abc import Callable
from pathlib import Path
from typing import Any

from distillation.contracts import SimulationCase
from thermodynamics.antoine_raoult import AntoineRecord, equilibrium_y

ROOT_TOLERANCE = 1e-4
Warnings = tuple[str, ...]
EquilibriumValue = tuple[float, float, Warnings]
StageRow = dict[str, Any]
LineGeometry = tuple[float, float, float, float]
TrialResult = tuple[float, list[StageRow], float, Warnings, LineGeometry]


class SimulationEngineNotReady(NotImplementedError):
    pass


def _records() -> tuple[list[AntoineRecord], AntoineRecord, str]:
    root = Path(__file__).resolve().parents[2]
    raw: dict[str, Any] = json.loads(
        (root / "data/thermodynamics/antoine_ethanol_water.json").read_text(encoding="utf-8")
    )
    if raw["status"] != "REVIEWED":
        raise ValueError("reviewed Antoine data is required")
    out: list[AntoineRecord] = []
    for x in raw["records"]:
        out.append(
            AntoineRecord(
                x["component"],
                x["A"],
                x["B"],
                x["C"],
                x["temperatureRange"]["min"],
                x["temperatureRange"]["max"],
                "K",
                "bar",
                x["provenance"]["citation"],
                x["provenance"]["publicationVersion"],
                x["provenance"]["reviewer"],
                x["provenance"]["reviewDate"],
            )
        )
    ethanol = [x for x in out if x.component == "ethanol"]
    water = next(x for x in out if x.component == "water")
    return ethanol, water, raw["dataVersion"]


def select_ethanol_record(records: list[AntoineRecord], temperature: float) -> AntoineRecord:
    """Deterministic approved-record rule: record 1 wins overlap."""
    for record in records:
        if record.temperature_min <= temperature <= record.temperature_max:
            return record
    if temperature > records[0].temperature_max and temperature <= records[1].temperature_max:
        return records[1]
    return records[0] if temperature < records[0].temperature_min else records[1]


def q_line_intersection(
    z_feed: float, q: float, rect_slope: float, rect_intercept: float
) -> tuple[float, float]:
    """Return the rectifying-line intersection with the approved q-line."""
    if abs(q - 1.0) < 1e-12:
        xq = z_feed
    else:
        # q/(q-1)*x - zF/(q-1) = mR*x + bR
        xq = (z_feed + (q - 1.0) * rect_intercept) / (q - (q - 1.0) * rect_slope)
    return xq, rect_slope * xq + rect_intercept


def _equilibrium_table(
    p: float, ethanol_records: list[AntoineRecord], heavy: AntoineRecord
) -> tuple[
    Callable[[float], EquilibriumValue],
    Callable[[float], tuple[float, Warnings]],
    list[dict[str, float]],
]:
    xs = [i / 400 for i in range(401)]
    values: list[EquilibriumValue] = []
    for x in xs:
        result = equilibrium_y(x, p, ethanol_records[0], heavy)
        selected = select_ethanol_record(ethanol_records, result[1])
        if selected is not ethanol_records[0]:
            result = equilibrium_y(x, p, selected, heavy)
        values.append(result)
    ys = [v[0] for v in values]
    warnings = tuple(sorted({w for v in values for w in v[2]}))

    def inverse(y: float) -> EquilibriumValue:
        if y < ys[0] - 1e-10 or y > ys[-1] + 1e-10:
            raise ValueError("NON_CONVERGED")
        if y <= ys[0]:
            return xs[0], values[0][1], warnings
        if y >= ys[-1]:
            return xs[-1], values[-1][1], warnings
        i = bisect_left(ys, y)
        y0, y1 = ys[i - 1], ys[i]
        f = (y - y0) / (y1 - y0)
        return (
            xs[i - 1] + f * (xs[i] - xs[i - 1]),
            values[i - 1][1] + f * (values[i][1] - values[i - 1][1]),
            warnings,
        )

    def value(x: float) -> tuple[float, Warnings]:
        if x <= xs[0]:
            return ys[0], values[0][2]
        if x >= xs[-1]:
            return ys[-1], values[-1][2]
        i = bisect_left(xs, x)
        f = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
        return ys[i - 1] + f * (ys[i] - ys[i - 1]), tuple(
            dict.fromkeys(values[i - 1][2] + values[i][2])
        )

    return inverse, value, [{"x_ethanol": xs[i], "y_ethanol": ys[i]} for i in range(0, 401, 20)]


def solve_mccabe_thiele(c: SimulationCase) -> dict[str, Any]:
    if c.condenser == "partial":
        raise SimulationEngineNotReady("NOT_IMPLEMENTED")
    ethanol_records, heavy, version = _records()
    F, z, D = c.F_kmol_h, c.zF_ethanol, c.D_kmol_h
    B = F - D
    inverse, equilibrium, curve = _equilibrium_table(c.P_bar, ethanol_records, heavy)
    if c.R <= 0:
        raise ValueError("R must be positive for total-condenser stepping")
    xlo, xhi = z, min(1.0, F * z / D)
    if xhi <= xlo:
        raise ValueError("ROOT_BRACKET_NOT_FOUND")

    def trial(xd: float) -> TrialResult:
        xb = (F * z - D * xd) / B
        rect_slope = c.R / (c.R + 1)
        rect_int = xd / (c.R + 1)
        xq, yq = q_line_intersection(z, c.q, rect_slope, rect_int)
        m2 = (yq - xb) / (xq - xb) if abs(xq - xb) > 1e-12 else rect_slope
        b2 = xb * (1 - m2)
        stages: list[StageRow] = []
        y = xd
        warnings: Warnings = ()
        for i in range(1, c.N + 1):
            x, t, w = inverse(y)
            warnings = tuple(dict.fromkeys(warnings + w))
            section = "rectifying" if i < c.NF else "stripping"
            y = rect_slope * x + rect_int if section == "rectifying" else m2 * x + b2
            stages.append(
                {"stage": i, "T_C": t - 273.15, "x_ethanol": x, "y_ethanol": y, "section": section}
            )
        ye, w = equilibrium(xb)
        warnings = tuple(dict.fromkeys(warnings + w))
        return y - ye, stages, xb, warnings, (xq, yq, m2, b2)

    prev: tuple[float, float] | None = None
    bracket: tuple[float, float] | None = None
    for i in range(51):
        x = xlo + (xhi - xlo) * i / 50
        r, *_ = trial(x)
        if prev and prev[1] * r <= 0:
            bracket = (prev[0], x)
            break
        prev = (x, r)
    if not bracket:
        raise ValueError("ROOT_BRACKET_NOT_FOUND")
    a, b = bracket
    for _ in range(80):
        m = (a + b) / 2
        rm = trial(m)[0]
        ra = trial(a)[0]
        if abs(rm) < 1e-8:
            a = b = m
            break
        if ra * rm <= 0:
            b = m
        else:
            a = m
    xd = (a + b) / 2
    outer, stages, xb, warnings, line_geometry = trial(xd)
    if abs(outer) > ROOT_TOLERANCE:
        raise ValueError("NON_CONVERGED")
    recovery = 100 * D * xd / (F * z)
    xq, yq, stripping_slope, stripping_intercept = line_geometry
    return {
        "status": "warning" if warnings else "success",
        "errorCode": None,
        "D_kmol_h": D,
        "B_kmol_h": B,
        "xD": xd,
        "xB": xb,
        "recovery_ethanol_percent": recovery,
        "thermoModel": "raoult-antoine",
        "thermoDataVersion": version,
        "isExtrapolated": bool(warnings),
        "warnings": list(warnings),
        "residuals": {
            "totalMass": 0.0,
            "ethanolBalance": 0.0,
            "outer": outer,
            "solver": abs(outer),
        },
        "QC_kW": None,
        "QR_kW": None,
        "heatLoss_kW": c.heatLoss_kW,
        "energyBreakdown": None,
        "operatingLines": {
            "rectifying": {"slope": c.R / (c.R + 1), "intercept": xd / (c.R + 1)},
            "qLine": {
                "vertical": abs(c.q - 1.0) < 1e-12,
                "slope": None if abs(c.q - 1.0) < 1e-12 else c.q / (c.q - 1.0),
                "intercept": None if abs(c.q - 1.0) < 1e-12 else -z / (c.q - 1.0),
            },
            "feedIntersection": {"x": xq, "y": yq},
            "stripping": {"slope": stripping_slope, "intercept": stripping_intercept},
            "equilibriumCurve": curve,
        },
        "stages": stages,
        "trace": ["total condenser", "direct NF section switch", "bisection outer xD solve"],
    }
