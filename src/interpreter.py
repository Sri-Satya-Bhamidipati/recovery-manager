import pandas as pd


def is_missing(value):
    return pd.isna(value) or value in ("", None)


def interpret_charge(charge, evidence):
    charge_type = charge["charge_type"]

    if charge_type == "lost_inbound":
        return interpret_lost_inbound(evidence)

    if charge_type == "damaged_in_warehouse":
        return interpret_damaged(evidence)

    if charge_type == "refund_issued_item_not_returned":
        return interpret_refund_not_returned(evidence)

    if charge_type == "inbound_defect_fee":
        return interpret_inbound_defect(evidence)

    if charge_type == "fulfilment_fee_weight_tier":
        return interpret_weight_tier(evidence)

    return {
        "interpretation": "UNCERTAIN",
        "reason": "Unknown charge type; no interpretation rule available.",
        "signals": [],
    }


def interpret_lost_inbound(evidence):
    receiving = evidence["receiving"]

    if not receiving:
        return {
            "interpretation": "INSUFFICIENT",
            "reason": "No receiving record available.",
            "signals": [],
        }

    record = receiving[0]

    ordered = record.get("qty_ordered")
    received = record.get("qty_received")

    if is_missing(ordered) or is_missing(received):
        return {
            "interpretation": "INSUFFICIENT",
            "reason": "Quantity information is incomplete.",
            "signals": [],
        }

    if received < ordered:
        return {
            "interpretation": "SUPPORTS",
            "reason": "Receiving evidence shows fewer units received than ordered.",
            "signals": [
                f"qty_ordered={ordered}",
                f"qty_received={received}",
            ],
        }

    return {
        "interpretation": "CONTRADICTS",
        "reason": "Receiving evidence shows no quantity shortfall.",
        "signals": [
            f"qty_ordered={ordered}",
            f"qty_received={received}",
        ],
    }


def interpret_damaged(evidence):
    receiving = evidence["receiving"]

    if not receiving:
        return {
            "interpretation": "INSUFFICIENT",
            "reason": "No receiving evidence available.",
            "signals": [],
        }

    record = receiving[0]

    carton_damage = record.get("carton_damage")
    unit_damage = record.get("unit_damage")
    quality = record.get("quality_flags")

    damage_signals = []

    for name, value in [
        ("carton_damage", carton_damage),
        ("unit_damage", unit_damage),
        ("quality_flags", quality),
    ]:
        if not is_missing(value) and value not in ("none", "nan"):
            damage_signals.append(f"{name}={value}")

    if damage_signals:
        return {
            "interpretation": "SUPPORTS",
            "reason": "Upstream receiving evidence contains a damage or quality signal.",
            "signals": damage_signals,
        }

    if carton_damage == "none" and unit_damage == "none":
        return {
            "interpretation": "CONTRADICTS",
            "reason": "Receiving evidence records no carton or unit damage.",
            "signals": [
                "carton_damage=none",
                "unit_damage=none",
            ],
        }

    return {
        "interpretation": "INSUFFICIENT",
        "reason": "Damage evidence is incomplete.",
        "signals": [],
    }


def interpret_inbound_defect(evidence):
    receiving = evidence["receiving"]

    if not receiving:
        return {
            "interpretation": "INSUFFICIENT",
            "reason": "No receiving evidence available.",
            "signals": [],
        }

    record = receiving[0]

    signals = []

    quality = record.get("quality_flags")
    unit_damage = record.get("unit_damage")
    carton_damage = record.get("carton_damage")

    if not is_missing(quality):
        signals.append(f"quality_flags={quality}")

    if unit_damage not in ("none", None) and not is_missing(unit_damage):
        signals.append(f"unit_damage={unit_damage}")

    if carton_damage not in ("none", None) and not is_missing(carton_damage):
        signals.append(f"carton_damage={carton_damage}")

    if signals:
        return {
            "interpretation": "SUPPORTS",
            "reason": "Receiving evidence contains a defect, damage, or quality signal.",
            "signals": signals,
        }

    if quality in (None, "nan") and unit_damage == "none" and carton_damage == "none":
        return {
            "interpretation": "CONTRADICTS",
            "reason": "Receiving evidence contains no recorded defect or damage signal.",
            "signals": [],
        }

    return {
        "interpretation": "INSUFFICIENT",
        "reason": "Available defect evidence is incomplete.",
        "signals": [],
    }


def interpret_refund_not_returned(evidence):
    returns = evidence["returns"]

    if not returns:
        return {
            "interpretation": "INSUFFICIENT",
            "reason": "No return record available.",
            "signals": [],
        }

    record = returns[0]

    state = record.get("observed_state")
    missing = record.get("parts_missing")
    disposition = record.get("operator_disposition")

    if state == "uncertain" or disposition == "pending_review":
        return {
            "interpretation": "UNCERTAIN",
            "reason": "Return evidence itself is uncertain or pending review.",
            "signals": [
                f"observed_state={state}",
                f"operator_disposition={disposition}",
            ],
        }

    signals = []

    if not is_missing(state):
        signals.append(f"observed_state={state}")

    if not is_missing(missing):
        signals.append(f"parts_missing={missing}")

    if not is_missing(disposition):
        signals.append(f"operator_disposition={disposition}")

    return {
        "interpretation": "INSUFFICIENT",
        "reason": (
            "Return evidence is available, but the fixture does not define "
            "an authoritative rule for deciding claimability."
        ),
        "signals": signals,
    }


def interpret_weight_tier(evidence):
    signals = []

    receiving = evidence["receiving"]
    prep = evidence["prep"]

    if receiving:
        record = receiving[0]

        ordered = record.get("qty_ordered")
        received = record.get("qty_received")

        if (
            not is_missing(ordered)
            and not is_missing(received)
            and received < ordered
        ):
            signals.append(
                f"receiving_quantity_gap={ordered - received}"
            )

        for name in ["carton_damage", "unit_damage", "quality_flags"]:
            value = record.get(name)

            if (
                not is_missing(value)
                and value not in ("none", "nan")
            ):
                signals.append(f"{name}={value}")

        if record.get("identity_match") == "uncertain":
            signals.append("identity_match=uncertain")

    if prep:
        record = prep[0]

        for name in [
            "original_barcode_covered",
            "fnsku_label_placement",
            "handling_marks",
        ]:
            value = record.get(name)

            if value in ("uncertain", "missing", "no", "some_missing"):
                signals.append(f"{name}={value}")

    if any("uncertain" in signal for signal in signals):
        return {
            "interpretation": "UNCERTAIN",
            "reason": "Upstream evidence contains uncertain fields relevant to the charge.",
            "signals": signals,
        }

    if signals:
        return {
            "interpretation": "SUPPORTS",
            "reason": "Upstream evidence contains anomalies associated with the unit.",
            "signals": signals,
        }

    return {
        "interpretation": "INSUFFICIENT",
        "reason": (
            "No direct contradictory evidence was found, but the synthetic "
            "fixture does not provide an authoritative rule for this charge."
        ),
        "signals": [],
    }

def is_claimable(charge, interpretation):
    charge_type = charge["charge_type"]
    result = interpretation["interpretation"]

    # Strong, charge-specific evidence
    if charge_type == "lost_inbound":
        return result == "SUPPORTS"

    if charge_type == "damaged_in_warehouse":
        return result == "SUPPORTS"

    if charge_type == "inbound_defect_fee":
        return result == "SUPPORTS"

    # We do NOT automatically claim these yet.
    # The synthetic fixture does not provide an authoritative
    # claimability rule for them.
    if charge_type in (
        "fulfilment_fee_weight_tier",
        "refund_issued_item_not_returned",
    ):
        return False

    return False