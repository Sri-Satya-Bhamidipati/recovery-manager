"""Presentation-only helpers: labels, signal tagging, explanatory copy.

Nothing here decides claimability. It only describes what the engine already
decided, using the engine's own interpretation status, reason and signals.
"""
from __future__ import annotations

import pandas as pd

DECISION_ORDER = ["CLAIM_CANDIDATE", "PENDING_REVIEW", "DO_NOT_CLAIM"]
INTERPRETATION_ORDER = ["SUPPORTS", "CONTRADICTS", "UNCERTAIN", "INSUFFICIENT"]
SOURCE_LABELS = {"receiving": "Receiving", "prep": "Prep", "pack": "Pack", "returns": "Returns"}

CHARGE_TYPE_LABELS = {
    "lost_inbound": "Lost inbound",
    "damaged_in_warehouse": "Damaged in warehouse",
    "inbound_defect_fee": "Inbound defect fee",
    "fulfilment_fee_weight_tier": "Fulfilment fee (weight tier)",
    "refund_issued_item_not_returned": "Refund issued, item not returned",
}

INTERPRETATION_HELP = {
    "SUPPORTS": "Upstream evidence is consistent with the charge being questionable.",
    "CONTRADICTS": "Upstream evidence disagrees with the charge being questionable.",
    "UNCERTAIN": "The evidence itself is ambiguous or flagged for review.",
    "INSUFFICIENT": "Evidence is missing, incomplete, or no authoritative rule exists.",
}

# Fields that identify a record rather than describe the unit's condition.
META_FIELDS = {"record_id", "unit_id", "org_id", "operator_id", "captured_at", "photo_refs"}


def label(value: str) -> str:
    """CLAIM_CANDIDATE -> CLAIM CANDIDATE."""
    return value.replace("_", " ")


def charge_type_label(value: str) -> str:
    return CHARGE_TYPE_LABELS.get(value, label(value).capitalize())


def money(value: float) -> str:
    return f"${value:,.2f}"


def is_blank(value) -> bool:
    return value is None or (not isinstance(value, str) and pd.isna(value)) or value == ""


def fmt_value(value) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def parse_signal(signal: str) -> tuple[str, str | None]:
    """'qty_received=22' -> ('qty_received', '22'). Derived signals have no value."""
    if "=" in signal:
        name, value = signal.split("=", 1)
        return name.strip(), value.strip()
    return signal.strip(), None


def tag_signal(status: str, signal: str) -> str:
    """Classify one engine signal as supports / contradicts / uncertain / observed.

    The engine returns signals as plain strings under an overall status. We
    inherit that status, except that individual values the engine itself treats
    as uncertain stay marked uncertain, and signals attached to an INSUFFICIENT
    result are only *observed* context (the engine drew no conclusion from them).
    """
    _, value = parse_signal(signal)
    if value in ("uncertain", "pending_review"):
        return "uncertain"
    if status == "SUPPORTS":
        return "supports"
    if status == "CONTRADICTS":
        return "contradicts"
    if status == "UNCERTAIN":
        return "observed"
    return "observed"


# Derived signals that point at real source columns.
DERIVED_SIGNAL_FIELDS = {"receiving_quantity_gap": ("qty_ordered", "qty_received")}


def cited_fields(result: dict) -> dict[str, dict[str, str]]:
    """{source: {field: kind}} for fields that the engine's signals point at.

    A field is cited only if the record actually holds that column with the
    signalled value (or the signal is a known derived signal over real columns).
    """
    status = result["interpretation"]["status"]
    cited: dict[str, dict[str, str]] = {}
    for sig in result["interpretation"]["signals"]:
        kind = tag_signal(status, sig)
        name, value = parse_signal(sig)
        for source, records in result["evidence"].items():
            if not records:
                continue
            record = records[0]
            if name in DERIVED_SIGNAL_FIELDS:
                if source == "receiving":
                    for f in DERIVED_SIGNAL_FIELDS[name]:
                        cited.setdefault(source, {}).setdefault(f, kind)
            elif name in record and not is_blank(record[name]) and fmt_value(record[name]) == value:
                cited.setdefault(source, {}).setdefault(name, kind)
    return cited


def decision_explanation(result: dict) -> tuple[str, str]:
    """(headline, body) describing the decision in plain language."""
    decision = result["decision"]
    status = result["interpretation"]["status"]

    if decision == "CLAIM_CANDIDATE":
        return (
            "Claim candidate",
            "Upstream evidence supports this charge and the engine has a claim rule for this "
            "charge type. It is queued as a candidate for recovery.",
        )
    if decision == "DO_NOT_CLAIM":
        return (
            "The system will not claim this charge",
            "Upstream evidence contradicts the charge, so the engine does not recommend a claim.",
        )
    # PENDING_REVIEW: intentional safety state, reason depends on interpretation.
    if status == "SUPPORTS":
        why = (
            "Evidence points to an anomaly, but the fixture defines no authoritative claim rule "
            "for this charge type, so the engine holds it rather than claiming."
        )
    elif status == "UNCERTAIN":
        why = "The upstream evidence is itself uncertain, so the engine will not guess."
    else:
        why = (
            "There is not enough evidence, or no authoritative rule, to decide either way, "
            "so the engine will not guess."
        )
    return (
        "The system cannot make a claim yet",
        why + " Routed to a human reviewer. Pending review is an intentional safety state, not a failure.",
    )
