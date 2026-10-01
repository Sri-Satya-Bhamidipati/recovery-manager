from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
UPSTREAM = DATA / "upstream"


def load():
    return {
        "fees": pd.read_csv(DATA / "fee_report_sample.csv"),
        "receiving": pd.read_csv(UPSTREAM / "receiving_sample.csv"),
        "prep": pd.read_csv(UPSTREAM / "prep_sample.csv"),
        "pack": pd.read_csv(UPSTREAM / "pack_sample.csv"),
        "returns": pd.read_csv(UPSTREAM / "returns_sample.csv"),
    }


def get_record(data, source, org_id, unit_id):
    df = data[source]

    return df[
        (df["org_id"] == org_id)
        & (df["unit_id"] == unit_id)
    ]


def main():
    data = load()

    target_types = [
        "damaged_in_warehouse",
        "fulfilment_fee_weight_tier",
    ]

    for charge_type in target_types:
        print("\n" + "=" * 70)
        print(charge_type.upper())
        print("=" * 70)

        charges = data["fees"][
            data["fees"]["charge_type"] == charge_type
        ]

        print(f"Fee lines: {len(charges)}")

        for _, charge in charges.iterrows():

            unit_id = charge["unit_id"]
            org_id = charge["org_id"]

            receiving = get_record(
                data, "receiving", org_id, unit_id
            )

            prep = get_record(
                data, "prep", org_id, unit_id
            )

            pack = get_record(
                data, "pack", org_id, unit_id
            )

            returns = get_record(
                data, "returns", org_id, unit_id
            )

            print(
                f"\n{charge['line_id']} | "
                f"{unit_id} | "
                f"${charge['amount_usd']}"
            )

            if not receiving.empty:
                r = receiving.iloc[0]

                print(
                    "  RECEIVING:",
                    f"qty {r['qty_received']}/{r['qty_ordered']},",
                    f"identity={r['identity_match']},",
                    f"carton_damage={r['carton_damage']},",
                    f"unit_damage={r['unit_damage']},",
                    f"quality={r['quality_flags']}"
                )

            if not prep.empty:
                p = prep.iloc[0]

                print(
                    "  PREP:",
                    f"barcode={p['original_barcode_covered']},",
                    f"label={p['fnsku_label_placement']},",
                    f"handling={p['handling_marks']}"
                )

            if not pack.empty:
                print(
                    "  PACK:",
                    "record present"
                )

            if not returns.empty:
                t = returns.iloc[0]

                print(
                    "  RETURNS:",
                    f"state={t['observed_state']},",
                    f"missing={t['parts_missing']},",
                    f"disposition={t['operator_disposition']}"
                )


if __name__ == "__main__":
    main()