"""HTML builders for the Recovery Manager UI (rendered via st.markdown)."""
from __future__ import annotations

from html import escape

import pandas as pd

import theme
from viewmodel import (
    DECISION_ORDER,
    INTERPRETATION_ORDER,
    INTERPRETATION_HELP,
    META_FIELDS,
    SOURCE_LABELS,
    charge_type_label,
    cited_fields,
    decision_explanation,
    fmt_value,
    is_blank,
    label,
    money,
    tag_signal,
)


def compact(html: str) -> str:
    """Strip indentation/blank lines so Markdown never treats HTML as a code block."""
    return "".join(line.strip() for line in html.splitlines() if line.strip())


def e(value) -> str:
    return escape(str(value))


# ---------------------------------------------------------------- atoms
def decision_badge(decision: str) -> str:
    return f'<span class="rm-badge {e(decision)}">{e(label(decision))}</span>'


def interp_badge(status: str) -> str:
    return f'<span class="rm-interp {e(status)}"><i></i>{e(status)}</span>'


def section_title(text: str) -> str:
    return f'<div class="rm-h2">{e(text)}</div>'


def page_header(eyebrow: str, title: str, lede: str) -> str:
    return compact(
        f"""<div class="rm-eyebrow">{e(eyebrow)}</div>
        <div class="rm-title">{e(title)}</div>
        <div class="rm-lede">{e(lede)}</div>"""
    )


# ---------------------------------------------------------------- overview
def kpi_row(metrics: dict, queue: pd.DataFrame) -> str:
    total = metrics["total_charges"]
    pct = lambda n: f"{(n / total * 100):.0f}% of records" if total else "–"
    cand = queue[queue.decision == "CLAIM_CANDIDATE"]
    zero_cand = int((cand.amount_usd == 0).sum())
    cand_note = f"Across {len(cand)} candidates"
    if zero_cand:
        cand_note += f"; {zero_cand} carry a $0.00 line amount"

    cards = [
        ("", "Charge records", f"{total}", "Fee lines processed"),
        ("", "Total charge amount", money(metrics["evaluated_amount_usd"]), "Synthetic fixture amounts"),
        ("accent", "Claim candidates", f"{metrics['claim_candidates']}", pct(metrics["claim_candidates"])),
        ("hold", "Pending review", f"{metrics['pending_review']}", f"{pct(metrics['pending_review'])} · intentional hold"),
        ("neg", "Do not claim", f"{metrics['do_not_claim']}", f"{pct(metrics['do_not_claim'])} · evidence contradicts"),
        ("accent", "Candidate amount", money(metrics["claim_amount_usd"]), cand_note),
    ]
    inner = "".join(
        f'<div class="rm-kpi {cls}"><div class="rm-eyebrow">{e(lab)}</div>'
        f'<div class="v">{e(val)}</div><div class="s">{e(sub)}</div></div>'
        for cls, lab, val, sub in cards
    )
    return f'<div class="rm-kpis">{inner}</div>'


DECISION_COLOR = {"CLAIM_CANDIDATE": theme.TERRACOTTA, "PENDING_REVIEW": theme.SAND, "DO_NOT_CLAIM": theme.SAGE}
INTERP_COLOR = {
    "SUPPORTS": theme.SAGE,
    "CONTRADICTS": theme.TERRACOTTA_DEEP,
    "UNCERTAIN": theme.SAND,
    "INSUFFICIENT": "#B9B5A6",
}
DECISION_HELP = {
    "CLAIM_CANDIDATE": "Evidence supports the charge and a claim rule exists",
    "PENDING_REVIEW": "Held for a human: uncertain, insufficient, or no authoritative rule",
    "DO_NOT_CLAIM": "Upstream evidence contradicts the charge",
}


def bars(rows: list[tuple[str, int, float, str, str]], total: int) -> str:
    """rows: (label, count, amount, color, help)."""
    out = []
    for lab, count, amount, color, hlp in rows:
        width = (count / total * 100) if total else 0
        out.append(
            f'<div class="rm-bar"><div class="t"><b>{e(lab)}</b><span>{count} · {money(amount)}</span></div>'
            f'<div class="track"><div class="fill" style="width:{width:.1f}%;background:{color}"></div></div>'
            f'<div class="h">{e(hlp)}</div></div>'
        )
    return f'<div class="rm-bars">{"".join(out)}</div>'


def decision_bars(queue: pd.DataFrame) -> str:
    rows = []
    for d in DECISION_ORDER:
        sub = queue[queue.decision == d]
        rows.append((label(d), len(sub), float(sub.amount_usd.sum()), DECISION_COLOR[d], DECISION_HELP[d]))
    return bars(rows, len(queue))


def interpretation_bars(queue: pd.DataFrame) -> str:
    rows = []
    for s in INTERPRETATION_ORDER:
        sub = queue[queue.interpretation == s]
        rows.append((s, len(sub), float(sub.amount_usd.sum()), INTERP_COLOR[s], INTERPRETATION_HELP[s]))
    return bars(rows, len(queue))


def _cell(n: int) -> str:
    return f'<td class="num{" zero" if n == 0 else ""}">{n}</td>'


def crosstab_html(queue: pd.DataFrame) -> str:
    head = "".join(f'<th class="num">{e(label(d))}</th>' for d in DECISION_ORDER)
    body = []
    for s in INTERPRETATION_ORDER:
        sub = queue[queue.interpretation == s]
        cells = "".join(_cell(int((sub.decision == d).sum())) for d in DECISION_ORDER)
        body.append(f"<tr><td>{interp_badge(s)}</td>{cells}<td class='num'>{len(sub)}</td></tr>")
    return (
        f'<div class="rm-table-wrap"><table class="rm-table"><tr><th>Interpretation</th>{head}'
        f'<th class="num">Total</th></tr>{"".join(body)}</table></div>'
    )


def by_type_html(queue: pd.DataFrame) -> str:
    head = "".join(f'<th class="num">{e(label(d))}</th>' for d in DECISION_ORDER)
    body = []
    for ct, sub in queue.groupby("charge_type"):
        cells = "".join(_cell(int((sub.decision == d).sum())) for d in DECISION_ORDER)
        body.append(
            f"<tr><td>{e(charge_type_label(ct))}<div class='rm-aside' style='margin:0'>"
            f"<span class='mono'>{e(ct)}</span></div></td>{cells}"
            f"<td class='num'>{len(sub)}</td><td class='num'>{money(float(sub.amount_usd.sum()))}</td></tr>"
        )
    return (
        f'<div class="rm-table-wrap"><table class="rm-table"><tr><th>Charge type</th>{head}'
        f'<th class="num">Records</th><th class="num">Amount</th></tr>{"".join(body)}</table></div>'
    )


# ---------------------------------------------------------------- trace
def _fact(k: str, v, cls: str = "") -> str:
    return f'<div class="rm-fact"><div class="k">{e(k)}</div><div class="v {cls}">{e(v)}</div></div>'


def _source_panel(source: str, records: list[dict], cited: dict[str, str]) -> str:
    name = SOURCE_LABELS[source]
    if not records:
        return (
            f'<div class="rm-src empty"><div class="rm-src-head"><b>{name}</b><span>no record</span></div>'
            f'<div class="none">No {name.lower()} record exists in the data for this '
            f"org_id + unit_id. Nothing is inferred.</div></div>"
        )

    record = records[0]
    extra = f" · +{len(records) - 1} more" if len(records) > 1 else ""
    fields = [(k, v) for k, v in record.items() if not is_blank(v)]
    blanks = [k for k, v in record.items() if is_blank(v)]
    # Cited fields first, then condition fields, then record metadata.
    fields.sort(key=lambda kv: (kv[0] not in cited, kv[0] in META_FIELDS))

    rows = []
    for k, v in fields:
        if k in cited:
            kind = cited[k]
            rows.append(
                f'<tr class="cited k-{kind}"><th>{e(k)}</th><td>{e(fmt_value(v))}'
                f'<span class="tag">{e(kind)}</span></td></tr>'
            )
        else:
            meta = " meta" if k in META_FIELDS else ""
            rows.append(f'<tr class="{meta.strip()}"><th>{e(k)}</th><td>{e(fmt_value(v))}</td></tr>')

    blank_line = (
        f'<div class="rm-blank">Blank in source: {e(", ".join(blanks))}</div>' if blanks else ""
    )
    return (
        f'<div class="rm-src"><div class="rm-src-head"><b>{name}</b>'
        f'<span>{e(record.get("record_id", ""))}{extra}</span></div>'
        f'<table class="rm-kv">{"".join(rows)}</table>{blank_line}</div>'
    )


def _signals_html(result: dict) -> str:
    status = result["interpretation"]["status"]
    signals = result["interpretation"]["signals"]
    if not signals:
        return (
            '<div class="rm-aside" style="margin-top:0">The engine produced no signals for this '
            "charge. It had no field-level evidence to cite.</div>"
        )
    chips = "".join(
        f'<span class="rm-sig {tag_signal(status, s)}">{e(s)}<small>{e(tag_signal(status, s))}</small></span>'
        for s in signals
    )
    return f'<div class="rm-sigs">{chips}</div>'


def _peers_html(result: dict, all_results: list[dict]) -> str:
    unit = result["unit"]["unit_id"]
    peers = [
        r for r in all_results
        if r["unit"]["unit_id"] == unit and r["charge"]["line_id"] != result["charge"]["line_id"]
    ]
    if not peers:
        return ""
    items = " ".join(
        f'<code>{e(p["charge"]["line_id"])}</code> {e(charge_type_label(p["charge"]["charge_type"]))} '
        f'· {e(label(p["decision"]).title())}'
        + ("; " if i < len(peers) - 1 else "")
        for i, p in enumerate(peers)
    )
    return f'<div class="rm-peers">Other charges on this unit: {items}</div>'


def trace_html(result: dict, all_results: list[dict]) -> str:
    ch, unit, interp = result["charge"], result["unit"], result["interpretation"]
    fee = result.get("fee_row", {})
    cited = cited_fields(result)
    headline, body = decision_explanation(result)

    # 1 charge
    charge_facts = [
        _fact("Charge ID", ch["line_id"], "mono"),
        _fact("Charge type", charge_type_label(ch["charge_type"])),
        _fact("Amount", money(float(ch["amount_usd"])), "big"),
    ]
    for key, lab in [("report_type", "Report"), ("posted_date", "Posted"), ("quantity", "Qty")]:
        if key in fee:
            charge_facts.append(_fact(lab, label(str(fee[key])) if key == "report_type" else fmt_value(fee[key])))

    # 2 unit
    present = {s: len(r) for s, r in result["evidence"].items()}
    counts = " · ".join(f"{SOURCE_LABELS[s]} {n}" for s, n in present.items())
    unit_facts = [_fact("org_id", unit["org_id"], "mono"), _fact("unit_id", unit["unit_id"], "mono")]
    for key in ("sku", "fnsku", "fba_shipment_id", "order_id"):
        if key in fee:
            unit_facts.append(_fact(key, fee[key], "mono"))

    panels = "".join(_source_panel(s, result["evidence"][s], cited.get(s, {})) for s in SOURCE_LABELS_KEYS)

    legend = (
        '<div class="rm-legend"><span class="supports">Supports the charge</span>'
        '<span class="contradicts">Contradicts it</span><span class="uncertain">Uncertain</span>'
        '<span class="observed">Observed, no conclusion drawn</span>'
        '<span class="nodata">No record / missing evidence</span></div>'
    )

    steps = [
        ("1", "Charge", f'<div class="rm-facts">{"".join(charge_facts)}</div>', ""),
        (
            "2",
            "Unit",
            f'<div class="rm-facts">{"".join(unit_facts)}</div>'
            f'<div class="rm-aside">Matched on org_id + unit_id. Evidence found: {e(counts)}.</div>'
            + _peers_html(result, all_results),
            "",
        ),
        (
            "3",
            "Upstream evidence",
            f'<div class="rm-sources">{panels}</div>'
            f'<div class="rm-signal-heading">Signals read from these records</div>{_signals_html(result)}{legend}',
            "",
        ),
        (
            "4",
            "Interpretation",
            f'<div class="rm-interp-box">{interp_badge(interp["status"])}'
            f'<div class="reason">{e(interp["reason"])}</div>'
            f'<div class="help">{e(INTERPRETATION_HELP[interp["status"]])}</div></div>',
            "",
        ),
        (
            "5",
            "Decision",
            f'<div class="rm-decision {e(result["decision"])}">{decision_badge(result["decision"])}'
            f'<div class="hl">{e(headline)}</div><p>{e(body)}</p></div>',
            "final",
        ),
    ]
    flow = "".join(
        f'<div class="rm-step {cls}"><div class="rm-node">{n}</div><div><h4>{e(t)}</h4>{content}</div></div>'
        for n, t, content, cls in steps
    )

    header = (
        f'<div class="rm-head"><div><div class="rm-eyebrow">Evidence trace</div>'
        f'<div class="id">{e(ch["line_id"])}</div>'
        f'<div class="sub">{e(charge_type_label(ch["charge_type"]))} · {e(unit["unit_id"])} · '
        f'{money(float(ch["amount_usd"]))}</div></div>'
        f'<div class="badges">{interp_badge(interp["status"])}{decision_badge(result["decision"])}</div></div>'
    )
    return compact(header + flow)


SOURCE_LABELS_KEYS = list(SOURCE_LABELS)


def preview_html(result: dict) -> str:
    """Compact trace summary shown under the queue table."""
    ch, interp = result["charge"], result["interpretation"]
    headline, body = decision_explanation(result)
    return compact(
        f"""<div class="rm-head" style="margin-top:1.2rem">
        <div><div class="rm-eyebrow">Selected charge</div><div class="id">{e(ch["line_id"])}</div>
        <div class="sub">{e(charge_type_label(ch["charge_type"]))} · {e(result["unit"]["unit_id"])} · {money(float(ch["amount_usd"]))}</div></div>
        <div class="badges">{interp_badge(interp["status"])}{decision_badge(result["decision"])}</div></div>
        <div class="rm-interp-box"><div class="rm-eyebrow">Why</div><div class="reason">{e(interp["reason"])}</div></div>
        <div style="height:.8rem"></div>
        {_signals_html(result)}
        <div style="height:.8rem"></div>
        <div class="rm-decision {e(result["decision"])}"><div class="hl" style="margin-top:0">{e(headline)}</div><p>{e(body)}</p></div>"""
    )
