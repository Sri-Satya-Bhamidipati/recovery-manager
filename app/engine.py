"""Thin adapter between the Streamlit UI and the existing decision engine.

No business rules live here. Every interpretation and decision comes from
``src/interpreter.py`` and ``src/main.py``; this module only calls them and
reshapes the output for display.
"""
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from loader import load_data
from main import process_charge, calculate_metrics

SOURCES = ["receiving", "prep", "pack", "returns"]


def run_pipeline() -> dict:
    """Run the existing engine over every fee line and return UI-ready data."""
    data = load_data()

    results = []
    for _, charge in data["fees"].iterrows():
        result = process_charge(data, charge)
        # Raw fee-report fields that process_charge does not carry through.
        result["fee_row"] = {k: v for k, v in charge.to_dict().items() if not pd.isna(v)}
        results.append(result)

    return {
        "results": results,
        "metrics": calculate_metrics(results),
        "queue": build_queue_frame(results),
    }


def build_queue_frame(results: list[dict]) -> pd.DataFrame:
    rows = []
    for r in results:
        rows.append(
            {
                "line_id": r["charge"]["line_id"],
                "unit_id": r["unit"]["unit_id"],
                "org_id": r["unit"]["org_id"],
                "charge_type": r["charge"]["charge_type"],
                "amount_usd": float(r["charge"]["amount_usd"]),
                "interpretation": r["interpretation"]["status"],
                "decision": r["decision"],
                "n_signals": len(r["interpretation"]["signals"]),
            }
        )
    return pd.DataFrame(rows)
