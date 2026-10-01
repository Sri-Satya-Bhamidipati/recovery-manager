from loader import load_data, get_unit_evidence
from interpreter import interpret_charge


def decide_claim(charge, interpreted):
    interpretation = interpreted["interpretation"]

    if interpretation == "CONTRADICTS":
        return "DO_NOT_CLAIM"

    if interpretation in ("UNCERTAIN", "INSUFFICIENT"):
        return "PENDING_REVIEW"

    if interpretation == "SUPPORTS":
        from interpreter import is_claimable

        if is_claimable(charge, interpreted):
            return "CLAIM_CANDIDATE"

        return "PENDING_REVIEW"

    return "PENDING_REVIEW"

def process_charge(data, charge):
    org_id = charge["org_id"]
    unit_id = charge["unit_id"]

    evidence = get_unit_evidence(
        data,
        org_id,
        unit_id,
    )

    interpretation = interpret_charge(
        charge,
        evidence,
    )

    decision = decide_claim(
        charge,
        interpretation,
    )

    return {
        "charge": {
            "line_id": charge["line_id"],
            "charge_type": charge["charge_type"],
            "amount_usd": charge["amount_usd"],
        },

        "unit": {
            "org_id": org_id,
            "unit_id": unit_id,
        },

        "evidence": evidence,

        "interpretation": {
            "status": interpretation["interpretation"],
            "reason": interpretation["reason"],
            "signals": interpretation["signals"],
        },

        "decision": decision,
    }

def print_result(result):
    charge = result["charge"]
    unit = result["unit"]
    interpretation = result["interpretation"]
    decision = result["decision"]

    print("\n" + "-" * 70)

    print(
        f"{charge['line_id']} | "
        f"{unit['unit_id']} | "
        f"${charge['amount_usd']}"
    )

    print(f"Charge:         {charge['charge_type']}")
    print(f"Interpretation: {interpretation['status']}")
    print(f"Decision:       {decision}")
    print(f"Reason:         {interpretation['reason']}")

    if interpretation["signals"]:
        print("Signals:")
        for signal in interpretation["signals"]:
            print(f"  - {signal}")

def calculate_metrics(results):
    total_charges = len(results)

    claim_candidates = [
        r for r in results
        if r["decision"] == "CLAIM_CANDIDATE"
    ]

    do_not_claim = [
        r for r in results
        if r["decision"] == "DO_NOT_CLAIM"
    ]

    pending_review = [
        r for r in results
        if r["decision"] == "PENDING_REVIEW"
    ]

    claim_amount = sum(
        float(r["charge"]["amount_usd"])
        for r in claim_candidates
    )

    evaluated_amount = sum(
        float(r["charge"]["amount_usd"])
        for r in results
    )

    interpretation_counts = {}

    for result in results:
        status = result["interpretation"]["status"]
        interpretation_counts[status] = (
            interpretation_counts.get(status, 0) + 1
        )

    return {
        "total_charges": total_charges,
        "claim_candidates": len(claim_candidates),
        "do_not_claim": len(do_not_claim),
        "pending_review": len(pending_review),
        "claim_amount_usd": claim_amount,
        "evaluated_amount_usd": evaluated_amount,
        "interpretation_counts": interpretation_counts,
    }

def main():
    data = load_data()

    print("=" * 70)
    print("RECOVERY MANAGER")
    print("=" * 70)

    print(f"Fee lines: {len(data['fees'])}")

    results = []

    for _, charge in data["fees"].iterrows():
        result = process_charge(data, charge)
        results.append(result)

    metrics = calculate_metrics(results)

    print("\n" + "=" * 70)
    print("RECOVERY METRICS")
    print("=" * 70)

    print(f"Total charge amount:     ${metrics['evaluated_amount_usd']:.2f}")
    print(f"Charge records:          {metrics['total_charges']}")
    print(f"Claim candidates:        {metrics['claim_candidates']}")
    print(f"Do not claim:            {metrics['do_not_claim']}")
    print(f"Pending review:          {metrics['pending_review']}")
    print(f"Candidate amount:        ${metrics['claim_amount_usd']:.2f}")

    print("\nPROCESSING COMPLETE")

    for result in results:
        print_result(result)

    print("\n" + "=" * 70)
    print("DECISION SUMMARY")
    print("=" * 70)

    decision_counts = {}

    for result in results:
        decision = result["decision"]
        decision_counts[decision] = decision_counts.get(decision, 0) + 1

    for decision, count in decision_counts.items():
        print(f"{decision:20} {count}")

    print("\n" + "=" * 70)
    print("INTERPRETATION SUMMARY")
    print("=" * 70)

    interpretation_counts = {}

    for result in results:
        interpretation = result["interpretation"]["status"]
        interpretation_counts[interpretation] = (
            interpretation_counts.get(interpretation, 0) + 1
        )

    for interpretation, count in interpretation_counts.items():
        print(f"{interpretation:20} {count}")


if __name__ == "__main__":
    main()