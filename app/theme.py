"""Palette and global CSS for the Recovery Manager UI."""

TERRACOTTA = "#BF897F"
SAND = "#DAC2B2"
CREAM = "#F7F2E0"
SAGE = "#707B6D"
CHARCOAL = "#3A3D3A"

# Derived tones (tints/shades of the palette) for text contrast and surfaces.
TERRACOTTA_DEEP = "#8C5A50"
SAGE_DEEP = "#4F5A4D"
SURFACE = "#FFFEFA"
RULE = "#D9D1C4"
MUTED = "#68706A"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

.stApp {{ background:{CREAM}; color:{CHARCOAL}; font-family:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif; }}
header[data-testid="stHeader"] {{ background:transparent; }}
.block-container {{ padding-top:2rem; padding-bottom:3.5rem; max-width:1320px; }}
h1,h2,h3 {{ font-family:'IBM Plex Sans',sans-serif !important; font-weight:600 !important; letter-spacing:0; color:{CHARCOAL}; }}
section[data-testid="stSidebar"] {{ background:{CHARCOAL}; border-right:0; }}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{ padding:1.35rem 1rem; }}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color:{CREAM}; }}

/* ---------- sidebar ---------- */
.rm-brand {{ font-family:'IBM Plex Sans',sans-serif; font-size:1.25rem; font-weight:600; line-height:1.15; color:{CREAM}; }}
.rm-brand small {{ display:block; font-family:'IBM Plex Sans',sans-serif; font-size:.65rem; letter-spacing:.12em; text-transform:uppercase; color:{SAND}; margin-top:.45rem; }}
.rm-note {{ font-size:.74rem; line-height:1.5; color:#D2D0C8; border-top:1px solid #555954; padding-top:.9rem; margin-top:1.4rem; }}
.rm-note code {{ color:{CREAM}; }}
section[data-testid="stSidebar"] [data-testid="stRadio"] label {{ padding:.5rem .65rem; border-left:2px solid transparent; color:{CREAM}; }}
section[data-testid="stSidebar"] [data-testid="stRadio"] label p {{ color:{CREAM}; font-weight:500; }}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{ background:#4B504B; border-left-color:{TERRACOTTA}; }}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {{ color:#FFFFFF; }}

/* ---------- page header ---------- */
.rm-eyebrow {{ font-size:.66rem; letter-spacing:.12em; text-transform:uppercase; color:{SAGE_DEEP}; font-weight:600; }}
.rm-title {{ font-family:'IBM Plex Sans',sans-serif; font-size:2rem; font-weight:600; line-height:1.15; margin:.2rem 0 .45rem; letter-spacing:0; }}
.rm-lede {{ color:#555D57; font-size:.92rem; max-width:76ch; line-height:1.55; margin-bottom:1.25rem; }}
.rm-h2 {{ font-family:'IBM Plex Sans',sans-serif; font-size:1.12rem; font-weight:600; margin:1.8rem 0 .65rem; padding-bottom:.45rem; border-bottom:1px solid {RULE}; }}
.rm-banner {{ border:1px solid {RULE}; border-left:3px solid {TERRACOTTA}; background:{SURFACE}; padding:.7rem .9rem; font-size:.8rem; color:{MUTED}; margin-bottom:1.2rem; }}

/* ---------- KPIs ---------- */
.rm-kpis {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:1px; border:1px solid {RULE}; background:{RULE}; }}
.rm-kpi {{ padding:.9rem 1rem .95rem; background:{SURFACE}; }}
.rm-kpi:last-child {{ border-right:none; }}
.rm-kpi .v {{ font-family:'IBM Plex Sans',sans-serif; font-size:1.8rem; line-height:1.15; margin:.35rem 0 .25rem; font-weight:600; font-variant-numeric:tabular-nums; }}
.rm-kpi .s {{ font-size:.74rem; color:{MUTED}; line-height:1.35; }}
.rm-kpi.accent {{ box-shadow:inset 0 3px 0 {TERRACOTTA}; }}
.rm-kpi.hold {{ box-shadow:inset 0 3px 0 #B99775; background:#F1E8DC; }}
.rm-kpi.neg {{ box-shadow:inset 0 3px 0 {SAGE}; background:#EDF0EA; }}

/* ---------- bars ---------- */
.rm-bars {{ border:1px solid {RULE}; background:{SURFACE}; padding:.9rem 1rem .3rem; }}
.rm-bar {{ margin-bottom:.95rem; }}
.rm-bar .t {{ display:flex; justify-content:space-between; align-items:baseline; font-size:.8rem; margin-bottom:.3rem; }}
.rm-bar .t b {{ font-weight:600; letter-spacing:.04em; font-size:.74rem; }}
.rm-bar .t span {{ font-variant-numeric:tabular-nums; color:{MUTED}; }}
.rm-bar .track {{ height:7px; background:#E9E4DA; border:0; }}
.rm-bar .fill {{ height:100%; }}
.rm-bar .h {{ font-size:.72rem; color:{MUTED}; margin-top:.25rem; }}

/* ---------- tables ---------- */
table.rm-table {{ width:100%; border-collapse:collapse; background:{SURFACE}; border:1px solid {RULE}; font-size:.8rem; }}
.rm-table th {{ text-align:left; font-size:.64rem; letter-spacing:.09em; text-transform:uppercase; color:{SAGE_DEEP}; font-weight:600; padding:.55rem .7rem; border-bottom:1px solid {RULE}; background:#EFE8DC; }}
.rm-table td {{ padding:.48rem .7rem; border-bottom:1px solid #E9E4DA; font-variant-numeric:tabular-nums; }}
.rm-table tr:last-child td {{ border-bottom:none; }}
.rm-table .num {{ text-align:right; }}
.rm-table .zero {{ color:#B3AFA2; }}
.rm-table .mono {{ font-family:'IBM Plex Mono',monospace; font-size:.76rem; }}
.rm-table-wrap {{ overflow-x:auto; }}

/* ---------- badges ---------- */
.rm-badge {{ display:inline-block; font-size:.68rem; font-weight:600; letter-spacing:.09em; padding:.28rem .6rem; border:1px solid transparent; white-space:nowrap; }}
.rm-badge.CLAIM_CANDIDATE {{ background:{TERRACOTTA}; color:#2B2D2B; border-color:{TERRACOTTA}; }}
.rm-badge.PENDING_REVIEW {{ background:#F1E6DA; color:{CHARCOAL}; border:1px dashed #B79A86; }}
.rm-badge.DO_NOT_CLAIM {{ background:#5F6A5C; color:{CREAM}; border-color:#5F6A5C; }}
.rm-interp {{ display:inline-flex; align-items:center; gap:.4rem; font-size:.7rem; font-weight:600; letter-spacing:.09em; padding:.22rem .55rem; border:1px solid {RULE}; background:{SURFACE}; white-space:nowrap; }}
.rm-interp i {{ width:8px; height:8px; display:inline-block; }}
.rm-interp.SUPPORTS i {{ background:{SAGE}; }}
.rm-interp.CONTRADICTS i {{ background:{TERRACOTTA_DEEP}; }}
.rm-interp.UNCERTAIN i {{ background:{SAND}; border:1px solid #A98C78; }}
.rm-interp.INSUFFICIENT i {{ background:transparent; border:1px dashed {MUTED}; }}

/* ---------- evidence trace ---------- */
.rm-head {{ display:flex; align-items:flex-end; justify-content:space-between; flex-wrap:wrap; gap:1rem; margin-bottom:1.6rem; padding-bottom:1rem; border-bottom:1px solid {CHARCOAL}; }}
.rm-head .id {{ font-family:'Newsreader',Georgia,serif; font-size:2rem; line-height:1.1; }}
.rm-head .sub {{ color:{MUTED}; font-size:.86rem; margin-top:.25rem; }}
.rm-head .badges {{ display:flex; gap:.5rem; align-items:center; flex-wrap:wrap; }}

.rm-step {{ display:grid; grid-template-columns:30px minmax(0,1fr); column-gap:18px; position:relative; padding-bottom:1.7rem; }}
.rm-step:not(:last-child)::before {{ content:""; position:absolute; left:14px; top:30px; bottom:2px; width:1px; background:#C9BBA1; }}
.rm-step:not(:last-child)::after {{ content:""; position:absolute; left:10px; bottom:0; width:8px; height:8px; border-right:1px solid #C9BBA1; border-bottom:1px solid #C9BBA1; transform:rotate(45deg); background:{CREAM}; }}
.rm-node {{ width:29px; height:29px; display:flex; align-items:center; justify-content:center; font-family:'IBM Plex Mono',monospace; font-size:.74rem; border:1px solid {CHARCOAL}; background:{CREAM}; }}
.rm-step h4 {{ margin:.2rem 0 .65rem; font-size:.7rem; letter-spacing:.14em; text-transform:uppercase; color:{SAGE_DEEP}; font-weight:600; }}
.rm-step.final .rm-node {{ background:{CHARCOAL}; color:{CREAM}; }}

.rm-facts {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:.9rem 1.4rem; background:{SURFACE}; border:1px solid {RULE}; padding:.9rem 1.1rem; }}
.rm-fact .k {{ font-size:.66rem; letter-spacing:.1em; text-transform:uppercase; color:{MUTED}; }}
.rm-fact .v {{ font-size:.92rem; margin-top:.1rem; word-break:break-word; font-variant-numeric:tabular-nums; }}
.rm-fact .v.mono {{ font-family:'IBM Plex Mono',monospace; font-size:.82rem; }}
.rm-fact .v.big {{ font-family:'Newsreader',Georgia,serif; font-size:1.35rem; }}
.rm-aside {{ font-size:.78rem; color:{MUTED}; margin-top:.55rem; line-height:1.5; }}

.rm-sources {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(310px,1fr)); gap:.9rem; }}
.rm-src {{ background:{SURFACE}; border:1px solid {RULE}; }}
.rm-src-head {{ display:flex; justify-content:space-between; align-items:center; padding:.55rem .8rem; border-bottom:1px solid {RULE}; background:{CREAM}; }}
.rm-src-head b {{ font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; }}
.rm-src-head span {{ font-family:'IBM Plex Mono',monospace; font-size:.7rem; color:{MUTED}; }}
.rm-src.empty {{ background:#F0EAE0; border-style:dashed; }}
.rm-src .none {{ padding:.9rem .8rem 1rem; font-size:.8rem; color:{MUTED}; line-height:1.45; }}
table.rm-kv {{ width:100%; border-collapse:collapse; font-size:.78rem; }}
.rm-kv td, .rm-kv th {{ padding:.32rem .8rem; text-align:left; vertical-align:top; border-bottom:1px solid #EFE7D2; font-weight:400; }}
.rm-kv th {{ color:{MUTED}; font-family:'IBM Plex Mono',monospace; font-size:.72rem; width:42%; word-break:break-word; }}
.rm-kv td {{ word-break:break-word; font-variant-numeric:tabular-nums; }}
.rm-kv tr.cited td, .rm-kv tr.cited th {{ color:{CHARCOAL}; font-weight:500; }}
.rm-kv tr.k-supports {{ background:#E8EBE4; box-shadow:inset 3px 0 0 {SAGE}; }}
.rm-kv tr.k-contradicts {{ background:#F3E4DF; box-shadow:inset 3px 0 0 {TERRACOTTA_DEEP}; }}
.rm-kv tr.k-uncertain {{ background:#F1E4D6; box-shadow:inset 3px 0 0 #A98C78; }}
.rm-kv tr.k-observed {{ background:#EEEBE0; box-shadow:inset 3px 0 0 {MUTED}; }}
.rm-kv .tag {{ float:right; font-size:.6rem; letter-spacing:.1em; text-transform:uppercase; color:{MUTED}; font-family:'IBM Plex Sans',sans-serif; }}
.rm-kv tr.meta th, .rm-kv tr.meta td {{ color:#8D8F88; }}
.rm-blank {{ padding:.5rem .8rem .65rem; font-size:.72rem; color:#8D8F88; border-top:1px solid #EFE7D2; }}

.rm-legend {{ display:flex; flex-wrap:wrap; gap:.4rem 1.2rem; font-size:.74rem; color:{MUTED}; margin:.7rem 0 0; }}
.rm-legend span::before {{ content:""; display:inline-block; width:10px; height:10px; margin-right:.4rem; vertical-align:-1px; }}
.rm-legend .supports::before {{ background:{SAGE}; }}
.rm-legend .contradicts::before {{ background:{TERRACOTTA_DEEP}; }}
.rm-legend .uncertain::before {{ background:#A98C78; }}
.rm-legend .observed::before {{ background:{MUTED}; }}
.rm-legend .nodata::before {{ background:#E6D7C6; border:1px dashed #A98C78; }}

.rm-sigs {{ display:flex; flex-wrap:wrap; gap:.5rem; }}
.rm-sig {{ font-family:'IBM Plex Mono',monospace; font-size:.76rem; padding:.3rem .6rem; border:1px solid {RULE}; background:{SURFACE}; border-left-width:3px; }}
.rm-sig.supports {{ border-left-color:{SAGE}; }}
.rm-sig.contradicts {{ border-left-color:{TERRACOTTA_DEEP}; }}
.rm-sig.uncertain {{ border-left-color:#A98C78; background:#F7EEE3; }}
.rm-sig.observed {{ border-left-color:{MUTED}; }}
.rm-sig small {{ font-family:'IBM Plex Sans',sans-serif; font-size:.6rem; letter-spacing:.1em; text-transform:uppercase; color:{MUTED}; margin-left:.5rem; }}

.rm-interp-box {{ background:{SURFACE}; border:1px solid {RULE}; padding:.95rem 1.1rem; }}
.rm-interp-box .reason {{ margin-top:.65rem; font-size:.95rem; line-height:1.5; }}
.rm-interp-box .help {{ margin-top:.3rem; font-size:.78rem; color:{MUTED}; }}

.rm-decision {{ padding:1.05rem 1.2rem; border:1px solid {RULE}; background:{SURFACE}; }}
.rm-decision.CLAIM_CANDIDATE {{ border-left:4px solid {TERRACOTTA}; }}
.rm-decision.PENDING_REVIEW {{ border-left:4px dashed #B79A86; background:#F8F1E6; }}
.rm-decision.DO_NOT_CLAIM {{ border-left:4px solid #5F6A5C; }}
.rm-decision .hl {{ font-family:'IBM Plex Sans',sans-serif; font-size:1.12rem; font-weight:600; margin:.65rem 0 .25rem; }}
.rm-decision p {{ margin:0; font-size:.88rem; line-height:1.55; color:#4E514D; max-width:70ch; }}

.rm-peers {{ font-size:.78rem; color:{MUTED}; margin-top:.6rem; line-height:1.9; }}
.rm-peers code {{ font-family:'IBM Plex Mono',monospace; font-size:.72rem; background:{SURFACE}; border:1px solid {RULE}; padding:.1rem .35rem; color:{CHARCOAL}; }}

/* ---------- streamlit widget polish ---------- */
div[data-testid="stDataFrame"] {{ border:1px solid {RULE}; background:{SURFACE}; }}
.stButton > button {{ border-radius:2px; border:1px solid {CHARCOAL}; background:{CHARCOAL}; color:{CREAM}; font-weight:500; }}
.stButton > button:hover {{ background:{CHARCOAL}; color:{CREAM}; border-color:{CHARCOAL}; }}
div[data-baseweb="select"] > div, .stTextInput input {{ border-radius:2px !important; background:{SURFACE} !important; }}
label[data-testid="stWidgetLabel"] p {{ font-size:.7rem; letter-spacing:.1em; text-transform:uppercase; color:{SAGE_DEEP}; font-weight:600; }}

/* Keep the trace connected and legible without decorative card chrome. */
.rm-step {{ column-gap:14px; padding-bottom:1.35rem; }}
.rm-step:not(:last-child)::before {{ background:#A7A69A; }}
.rm-step:not(:last-child)::after {{ background:{CREAM}; border-color:#A7A69A; }}
.rm-node {{ background:#EEE8DC; border-color:#A8A398; font-weight:500; }}
.rm-step h4 {{ color:{CHARCOAL}; font-size:.67rem; letter-spacing:.12em; }}
.rm-signal-heading {{ margin:.85rem 0 .45rem; color:{MUTED}; font-size:.65rem; font-weight:600; letter-spacing:.1em; text-transform:uppercase; }}
.rm-src-head {{ background:#EFE8DC; }}
.rm-src-head span {{ color:{MUTED}; }}
.rm-kv tr.k-supports {{ background:#E8EEE7; }}
.rm-kv tr.k-contradicts {{ background:#F4E5E0; }}
.rm-kv tr.k-uncertain {{ background:#F3E8D8; }}
.rm-kv tr.k-observed {{ background:#F1F0EB; }}
.rm-blank {{ background:#F0EAE0; color:#675E54; }}
.rm-interp-box {{ border-left:3px solid {SAGE}; }}
.rm-decision.PENDING_REVIEW {{ background:#F3E8D8; border-color:#C9B194; border-left-style:solid; }}
.rm-badge {{ letter-spacing:.06em; padding:.26rem .52rem; }}

@media (max-width: 850px) {{
	.block-container {{ padding-top:1.35rem; }}
	.rm-kpis {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
	.rm-title {{ font-size:1.7rem; }}
	.rm-sources {{ grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); }}
}}
@media (max-width: 520px) {{
	.rm-kpis {{ grid-template-columns:1fr 1fr; }}
	.rm-kpi {{ padding:.75rem .7rem; }}
	.rm-kpi .v {{ font-size:1.45rem; }}
	.rm-facts {{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:.75rem; }}
}}
</style>
"""
