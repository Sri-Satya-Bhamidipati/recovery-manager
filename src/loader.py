from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
UPSTREAM_DIR = DATA_DIR / "upstream"


def load_data():
    return {
        "fees": pd.read_csv(DATA_DIR / "fee_report_sample.csv"),
        "receiving": pd.read_csv(UPSTREAM_DIR / "receiving_sample.csv"),
        "prep": pd.read_csv(UPSTREAM_DIR / "prep_sample.csv"),
        "pack": pd.read_csv(UPSTREAM_DIR / "pack_sample.csv"),
        "returns": pd.read_csv(UPSTREAM_DIR / "returns_sample.csv"),
    }


def get_unit_evidence(data, org_id, unit_id):
    evidence = {}

    for source in ["receiving", "prep", "pack", "returns"]:
        df = data[source]

        matches = df[
            (df["org_id"] == org_id)
            & (df["unit_id"] == unit_id)
        ]

        evidence[source] = matches.to_dict(orient="records")

    return evidence