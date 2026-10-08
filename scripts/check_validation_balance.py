"""Check whether a validation case is internally material-balanced.

This script is intentionally narrow: it checks only the ethanol component
balance for a binary Ethanol-Water case already mapped into the validation JSON.
It does not run the column model and does not mark validation PASS/FAIL.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class BalanceCheck:
    feed_ethanol: float
    distillate_ethanol: float
    bottoms_ethanol: float
    residual: float
    required_d_from_xd_xb: float
    recovery_from_input: float
    recovery_from_required_d: float
    xb_from_input_d: float

    @property
    def residual_abs(self) -> float:
        return abs(self.residual)


def _number(value: Any, label: str) -> float:
    if not isinstance(value, int | float):
        raise ValueError(f"{label} must be numeric")
    return float(value)


def check_case(case: dict[str, Any]) -> BalanceCheck:
    mapped = case["mappedInput"]
    observed = case["observed"]

    f = _number(mapped["F_kmol_h"], "F_kmol_h")
    zf = _number(mapped["zF_ethanol"], "zF_ethanol")
    d = _number(mapped["D_kmol_h"], "D_kmol_h")
    xd = _number(observed["xD_ethanol"]["value"], "observed.xD_ethanol.value")
    xb = _number(observed["xB_ethanol"]["value"], "observed.xB_ethanol.value")

    if d >= f:
        raise ValueError("D_kmol_h must be lower than F_kmol_h")
    if abs(xd - xb) < 1e-12:
        raise ValueError("xD and xB must be different to infer D")

    b = f - d
    feed_ethanol = f * zf
    distillate_ethanol = d * xd
    bottoms_ethanol = b * xb
    residual = feed_ethanol - distillate_ethanol - bottoms_ethanol

    required_d = f * (zf - xb) / (xd - xb)
    required_b = f - required_d
    recovery_from_input = 100 * distillate_ethanol / feed_ethanol
    recovery_from_required_d = 100 * required_d * xd / feed_ethanol
    xb_from_input_d = (feed_ethanol - d * xd) / b

    # Keep required_b computed for readability in derivation; the returned
    # values are enough for V1 diagnostics.
    _ = required_b

    return BalanceCheck(
        feed_ethanol=feed_ethanol,
        distillate_ethanol=distillate_ethanol,
        bottoms_ethanol=bottoms_ethanol,
        residual=residual,
        required_d_from_xd_xb=required_d,
        recovery_from_input=recovery_from_input,
        recovery_from_required_d=recovery_from_required_d,
        xb_from_input_d=xb_from_input_d,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "case_path",
        nargs="?",
        default=Path("data/validation/cases/ethanol-water.pending.json"),
        type=Path,
        help="Path to validation case JSON.",
    )
    args = parser.parse_args()
    case = json.loads(args.case_path.read_text(encoding="utf-8"))
    result = check_case(case)
    print(f"feed_ethanol_kmol_h={result.feed_ethanol:.6f}")
    print(f"distillate_ethanol_kmol_h={result.distillate_ethanol:.6f}")
    print(f"bottoms_ethanol_kmol_h={result.bottoms_ethanol:.6f}")
    print(f"ethanol_balance_residual={result.residual:.6f}")
    print(f"D_required_by_xD_xB={result.required_d_from_xd_xb:.6f}")
    print(f"recovery_from_input_D={result.recovery_from_input:.6f}")
    print(f"recovery_from_required_D={result.recovery_from_required_d:.6f}")
    print(f"xB_ethanol_if_input_D_is_kept={result.xb_from_input_d:.6f}")


if __name__ == "__main__":
    main()
