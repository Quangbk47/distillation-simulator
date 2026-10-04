import json
from pathlib import Path

from jsonschema import validate

ROOT = Path(__file__).resolve().parents[2]


def load_json(relative_path: str) -> dict[str, object]:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def test_reviewed_thermo_data_matches_schema() -> None:
    schema = load_json("data/thermodynamics/schema.json")
    data = load_json("data/thermodynamics/antoine_ethanol_water.json")
    validate(data, schema)
    assert data["status"] == "REVIEWED"
    assert {record["component"] for record in data["records"]} == {"ethanol", "water"}
    ethanol = [record for record in data["records"] if record["component"] == "ethanol"]
    water = [record for record in data["records"] if record["component"] == "water"]
    assert len(ethanol) == 2
    assert len(water) == 1
    assert all(
        record["provenance"]["url"].startswith("https://webbook.nist.gov/")
        for record in data["records"]
    )


def test_validation_case_uses_accepted_v1_threshold() -> None:
    schema = load_json("data/validation/schema.json")
    case = load_json("data/validation/cases/ethanol-water.pending.json")
    validate(case, schema)
    acceptance = case["validationAcceptance"]
    assert acceptance["metric"] == "MAE_xD_xB_percentage_points"
    assert acceptance["threshold"] == 5
    assert acceptance["pass"] is None
