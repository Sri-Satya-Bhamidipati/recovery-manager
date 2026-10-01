"""Recovery Manager: Streamlit UI over the existing deterministic engine.

Run from the repository root:  streamlit run app/app.py
"""
from __future__ import annotations

import streamlit as st

import engine
import theme
import widgets as w
from viewmodel import DECISION_ORDER, INTERPRETATION_ORDER, charge_type_label, label, money

st.set_page_config(page_title="Recovery Manager", page_icon="🧾", layout="wide")
st.markdown(theme.CSS, unsafe_allow_html=True)

VIEWS = ["Overview", "Recovery Queue", "Evidence Explorer"]


@st.cache_data(show_spinner="Running the recovery engine…")
def get_pipeline() -> dict:
    return engine.run_pipeline()


pipeline = get_pipeline()
results = pipeline["results"]
queue = pipeline["queue"]
metrics = pipeline["metrics"]
by_line = {r["charge"]["line_id"]: r for r in results}

st.session_state.setdefault("sel", results[0]["charge"]["line_id"] if results else None)


def goto_trace(line_id: str) -> None:
    st.session_state["sel"] = line_id
    st.session_state["nav"] = "Evidence Explorer"


def pick_from_explorer() -> None:
    st.session_state["sel"] = st.session_state["explorer_pick"]


# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.markdown(
        '<div class="rm-brand">Recovery Manager<small>Stage 5 · Claim decisions</small></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    view = st.radio("View", VIEWS, key="nav", label_visibility="collapsed")


# ------------------------------------------------------------------ overview
def render_overview() -> None:
    st.markdown(
        w.page_header(
            "Overview",
            "Recovery at a glance",
            "Recovery Manager connects reported charges to operational evidence and identifies "
            "claims that are supported, contradicted, or require review.",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(w.kpi_row(metrics, queue), unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown(w.section_title("Decisions"), unsafe_allow_html=True)
        st.markdown(w.decision_bars(queue), unsafe_allow_html=True)
    with right:
        st.markdown(w.section_title("Evidence interpretation"), unsafe_allow_html=True)
        st.markdown(w.interpretation_bars(queue), unsafe_allow_html=True)

    st.markdown(w.section_title("How interpretations become decisions"), unsafe_allow_html=True)
    st.markdown(w.crosstab_html(queue), unsafe_allow_html=True)
    st.markdown(
        '<div class="rm-aside">Supporting evidence is not automatically a claim. Where the fixture '
        "defines no authoritative rule for a charge type, SUPPORTS is still held as "
        "<b>pending review</b>. Pending review is an intentional safety state, not a failure.</div>",
        unsafe_allow_html=True,
    )

    st.markdown(w.section_title("By charge type"), unsafe_allow_html=True)
    st.markdown(w.by_type_html(queue), unsafe_allow_html=True)
    st.markdown(
        '<div class="rm-aside">Counts are computed from the fixture on every run. They describe '
        "engine output, not accuracy: the fixture is not a human-labelled evaluation set.</div>",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------ queue
DECISION_STYLE = {
    "CLAIM CANDIDATE": "background-color:#BF897F;color:#2B2D2B;font-weight:600",
    "PENDING REVIEW": "background-color:#F1E6DA;color:#3A3D3A;font-weight:600",
    "DO NOT CLAIM": "background-color:#5F6A5C;color:#F7F2E0;font-weight:600",
}
INTERP_STYLE = {
    "SUPPORTS": "color:#4F5A4D;font-weight:600",
    "CONTRADICTS": "color:#8C5A50;font-weight:600",
    "UNCERTAIN": "color:#7A6250;font-weight:600",
    "INSUFFICIENT": "color:#6E716B",
}


def render_queue() -> None:
    st.markdown(
        w.page_header(
            "Recovery queue",
            "Charges to review",
            "Search or filter the 61 processed charges, then select a row to see what the records say.",
        ),
        unsafe_allow_html=True,
    )

    counts = queue.decision.value_counts()
    options = {f"All · {len(queue)}": None}
    for d in DECISION_ORDER:
        options[f"{label(d).capitalize()} · {int(counts.get(d, 0))}"] = d
    chosen = st.segmented_control("Decision", list(options), default=list(options)[0], key="q_decision")
    decision_filter = options.get(chosen)

    c1, c2, c3 = st.columns([1.2, 1, 1.3])
    search = c1.text_input("Search", placeholder="line_id or unit_id", key="q_search").strip().lower()
    interp_filter = c2.multiselect("Interpretation", INTERPRETATION_ORDER, key="q_interp")
    type_filter = c3.multiselect(
        "Charge type",
        sorted(queue.charge_type.unique()),
        format_func=charge_type_label,
        key="q_type",
    )

    df = queue
    if decision_filter:
        df = df[df.decision == decision_filter]
    if interp_filter:
        df = df[df.interpretation.isin(interp_filter)]
    if type_filter:
        df = df[df.charge_type.isin(type_filter)]
    if search:
        df = df[df.line_id.str.lower().str.contains(search) | df.unit_id.str.lower().str.contains(search)]
    df = df.reset_index(drop=True)

    st.markdown(
        f'<div class="rm-aside" style="margin:.4rem 0 .5rem">Showing <b>{len(df)}</b> of {len(queue)} '
        f"records · {money(float(df.amount_usd.sum()))}</div>",
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No charges match these filters.")
        return

    shown = df[["line_id", "unit_id", "charge_type", "amount_usd", "interpretation", "decision"]].copy()
    shown["decision"] = shown.decision.map(label)
    styled = (
        shown.style.map(lambda v: DECISION_STYLE.get(v, ""), subset=["decision"])
        .map(lambda v: INTERP_STYLE.get(v, ""), subset=["interpretation"])
        .format({"amount_usd": "${:,.2f}"})
    )
    event = st.dataframe(
        styled,
        hide_index=True,
        width="stretch",
        height=min(38 * (len(shown) + 1) + 3, 460),
        on_select="rerun",
        selection_mode="single-row",
        key="queue_table",
    )

    rows = event.selection.rows if event and event.selection else []
    if not rows:
        st.markdown(
            '<div class="rm-banner" style="margin-top:1rem">Select a row to preview its trace here.</div>',
            unsafe_allow_html=True,
        )
        return

    line_id = df.iloc[rows[0]]["line_id"]
    st.session_state["sel"] = line_id
    st.markdown(w.preview_html(by_line[line_id]), unsafe_allow_html=True)
    st.write("")
    st.button("Open full evidence trace →", on_click=goto_trace, args=(line_id,), key="open_trace")


# ------------------------------------------------------------------ explorer
def render_explorer() -> None:
    st.markdown(
        w.page_header(
            "Evidence explorer",
            "Follow the evidence",
            "See the selected charge, its matched unit, each available upstream record, and the "
            "result. Missing records stay clearly marked as missing.",
        ),
        unsafe_allow_html=True,
    )

    ids = list(by_line)
    sel = st.session_state["sel"] if st.session_state["sel"] in by_line else ids[0]

    def fmt(line_id: str) -> str:
        r = by_line[line_id]
        return (
            f"{line_id} · {charge_type_label(r['charge']['charge_type'])} · "
            f"{money(float(r['charge']['amount_usd']))} · {label(r['decision'])}"
        )

    st.selectbox(
        "Charge",
        ids,
        index=ids.index(sel),
        format_func=fmt,
        key="explorer_pick",
        on_change=pick_from_explorer,
    )
    st.write("")
    st.markdown(w.trace_html(by_line[sel], results), unsafe_allow_html=True)


{"Overview": render_overview, "Recovery Queue": render_queue, "Evidence Explorer": render_explorer}[view]()
