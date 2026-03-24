"""results/ui.py — CSS injection and shared UI render helpers."""

import streamlit as st

from results.charts import fmt
from results.constants import ALT_COLORS, ALTERNATIVES

_CSS = """
<style>
.params-bar {
    display: flex; gap: 24px; flex-wrap: wrap;
    background: var(--secondary-background-color); border: 1px solid #d6ead7;
    border-radius: 10px; padding: 16px 24px; margin-bottom: 24px;
}
.params-item { display: flex; flex-direction: column; gap: 4px; }
.params-lbl {
    font-size: 12px; color: var(--text-color); letter-spacing: 1px;
    text-transform: uppercase; font-weight: 500;
}
.params-val { font-size: 16px; font-weight: 600; color: #119822; }
.crit-card {
    background: var(--secondary-background-color); border: 1px solid #e2e8e2;
    border-radius: 10px; padding: 16px 20px; margin-bottom: 10px;
}
.crit-head { display: flex; align-items: center; gap: 12px; }
.crit-dot  { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.crit-name { font-size: 16px; font-weight: 700; color: var(--text-color); flex: 1; }
.crit-pct  { font-size: 20px; font-weight: 700; }
.mini-bar-wrap {
    width: 70px; height: 6px; background: rgba(128,128,128,0.25);
    border-radius: 99px; overflow: hidden; margin-left: 8px;
}
.mini-bar-fill { height: 100%; border-radius: 99px; }
.sub-row { display: flex; align-items: center; gap: 12px; margin-top: 12px; }
.sub-name { font-size: 13px; color: var(--text-color); width: 160px; flex-shrink: 0; }
.sub-bar-wrap {
    flex: 1; height: 6px; background: rgba(128,128,128,0.2);
    border-radius: 99px; overflow: hidden;
}
.sub-bar-fill { height: 100%; border-radius: 99px; opacity: 0.8; }
.sub-val { font-size: 13px; color: var(--text-color); width: 52px; text-align: right; }
.heatmap-table-wrap { overflow-x: auto; }
.heatmap-table {
    width: 100%; border-collapse: collapse; font-size: 14px;
}
.heatmap-table th {
    padding: 10px 14px; color: var(--text-color); font-weight: 600; font-size: 13px;
    border-bottom: 1px solid #e0e0e0; text-align: center; white-space: nowrap;
}
.heatmap-table th:first-child { text-align: left; }
.heatmap-table td {
    padding: 9px 14px; text-align: center;
    font-size: 13px; white-space: nowrap; border-bottom: 1px solid #f0f0f0;
}
.heatmap-table td:first-child { text-align: left; color: var(--text-color); }
.heatmap-table tr.overall-row td {
    border-top: 2px solid #ccc; font-weight: 700; font-size: 14px;
}
[data-testid="stMetricValue"] {
    font-size: 16px !important;
}
</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def section_header(title: str) -> None:
    st.markdown(
        f"""
<div style="display:flex;align-items:center;gap:12px;">
  <div class="card-label">{title}</div>
  <div style="width:200px;height:1px;background:#2A7221;"></div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_params_bar(
    savings_target: float,
    time_horizon: int,
    monthly_income: float,
    monthly_spending: float,
    initial_wealth: float,
) -> None:
    items = [
        ("Savings Target", f"{fmt(savings_target)} USD"),
        ("Time Horizon", f"{time_horizon} months"),
        ("Monthly Income", f"{fmt(monthly_income)} USD"),
        ("Monthly Spending", f"{fmt(monthly_spending)} USD"),
        ("Initial Wealth", f"{fmt(initial_wealth)} USD"),
    ]
    cells = "".join(
        f'<div class="params-item">'
        f'<div class="params-lbl">{lbl}</div>'
        f'<div class="params-val">{val}</div>'
        f"</div>"
        for lbl, val in items
    )
    st.markdown(
        f'<div class="params-bar">{cells}</div>',
        unsafe_allow_html=True,
    )


def render_final_ranking(scores: dict[str, float]) -> None:

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Podium: silver | gold | bronze
    if len(ranked) >= 3:
        podium = [ranked[1], ranked[0], ranked[2]]
        heights = [90, 120, 70]
        rank_nums = [2, 1, 3]
    else:
        podium = ranked
        heights = [100] * len(ranked)
        rank_nums = list(range(1, len(ranked) + 1))

    # flex-end so bars grow upward from the same baseline
    podium_html = '<div style="display:flex;align-items:flex-end;gap:0;">'
    for (alt, score), h, rank in zip(podium, heights, rank_nums):
        bar_color = ALT_COLORS.get(alt, "#888")
        podium_html += (
            f'<div style="flex:1;display:flex;flex-direction:column;'
            f'align-items:center;">'
            f'<div style="font-size:14px;color:var(--text-color);margin-bottom:6px;'
            f'text-align:center;font-weight:500;">{alt}</div>'
            f'<div style="font-size:16px;font-weight:700;color:{bar_color};'
            f'margin-bottom:6px;">{score * 100:.1f}%</div>'
            f'<div style="width:100%;height:{h}px;background:{bar_color};'
            f"border-radius:6px 6px 0 0;display:flex;align-items:center;"
            f"justify-content:center;font-size:24px;font-weight:700;"
            f'color:#fff;box-shadow:0 2px 8px {bar_color}55;">#{rank}</div>'
            f"</div>"
        )
    podium_html += "</div>"
    st.markdown(podium_html, unsafe_allow_html=True)

    # 4th place — flex:1 so each card scales with page width
    if len(ranked) > 3:
        rest_html = '<div style="display:flex;gap:12px;">'
        for rank_n, (alt, score) in enumerate(ranked[3:], start=4):
            bar_color = ALT_COLORS.get(alt, "#888")
            rest_html += (
                f'<div style="flex:1;background:var(--secondary-background-color);'
                f"border:1px solid #e0e0e0;border-radius:8px;"
                f'padding:14px 16px;text-align:center;">'
                f'<div style="font-size:12px;color:var(--text-color);margin-bottom:4px;">'
                f"#{rank_n}</div>"
                f'<div style="font-size:15px;color:var(--text-color);font-weight:500;">'
                f"{alt}</div>"
                f'<div style="font-size:16px;font-weight:700;color:{bar_color};">'
                f"{score * 100:.1f}%</div>"
                f"</div>"
            )
        rest_html += "</div>"
        st.markdown(rest_html, unsafe_allow_html=True)


def render_monte_carlo_tab(
    alt: str,
    result: dict,
    goal: float,
    time_horizon: int,
) -> None:
    """Render metrics + 2 charts for one alternative inside a tab."""
    import numpy as np

    from results.charts import build_histogram, build_run_chart

    color = ALT_COLORS[alt]
    finals = result["finals"]
    n = len(finals)
    p10 = float(np.percentile(finals, 10))
    p50 = float(np.percentile(finals, 50))
    p90 = float(np.percentile(finals, 90))
    success_pct = float((finals >= goal).sum() / n * 100) if goal > 0 else 0.0
    std = float(np.std(finals))

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("P10 Terminal Wealth", f"{fmt(p10)} USD")
    m2.metric("Median Terminal Wealth", f"{fmt(p50)} USD")
    m3.metric("P90 Terminal Wealth", f"{fmt(p90)} USD")
    m4.metric("Terminal Wealth Std", f"{fmt(std)} USD")
    m5.metric("Probability >= Goal", f"{success_pct:.1f}%")

    st.markdown(
        f'<div style="font-size:14px;font-weight:600;color:{color};'
        f'margin:12px 0 4px;">Simulation Run Chart</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        build_run_chart(result, alt, time_horizon, goal),
        width="stretch",
        key=f"rc_{alt}",
    )

    st.markdown(
        f'<div style="font-size:14px;font-weight:600;color:{color};'
        f'margin:12px 0 4px;">Terminal Wealth Distribution</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        build_histogram(result, alt, goal),
        width="stretch",
        key=f"hc_{alt}",
    )


def render_ahp_criteria_cards(
    main_weights: dict[str, float],
    subs_by_parent: dict[str, dict[str, float]],
) -> None:
    from results.constants import CRIT_COLORS
    import streamlit as st

    # map internal names to display names (keeps previous behaviour)
    crit_display = {
        "Financial security": "Financial Security",
        "Personal characteristics": "Personal Characteristics",
        "Profitability": "Profitability",
        "Readiness": "Readiness",
    }

    sorted_main = sorted(main_weights.items(), key=lambda x: x[1], reverse=True)

    for raw_name, weight in sorted_main:
        # preserve display name and color mapping while looking up subcriteria by the raw key
        display_name = crit_display.get(raw_name, raw_name)
        color = CRIT_COLORS.get(display_name, "#119822")
        pct = weight * 100.0
        bar_w = int(pct)

        # subs_by_parent stores {criterion: {subname: local_weight}}
        subs = subs_by_parent.get(raw_name, {}) or {}

        # sort subcriteria by local weight descending and render rows
        sub_rows_html = "".join(
            f'<div class="sub-row">'
            f'  <div class="sub-name">{name}</div>'
            f'  <div class="sub-bar-wrap">'
            f'    <div class="sub-bar-fill" style="width:{int(lw * 100)}%;background:{color};"></div>'
            f"  </div>"
            f'  <div class="sub-val">{lw:.4f}</div>'
            f"</div>"
            for name, lw in sorted(subs.items(), key=lambda x: x[1], reverse=True)
        )

        st.markdown(
            f"""
<div class="crit-card">
  <div class="crit-head">
    <div class="crit-dot" style="background:{color};"></div>
    <div class="crit-name">{display_name}</div>
    <div class="crit-pct" style="color:{color};">{pct:.1f}%</div>
    <div class="mini-bar-wrap">
      <div class="mini-bar-fill" style="width:{bar_w}%;background:{color};"></div>
    </div>
  </div>
  {sub_rows_html}
</div>
""",
            unsafe_allow_html=True,
        )


def render_ahp_heatmap(score_matrix_or_scores, ranking_df=None) -> None:
    """
    Renders a heatmap table of sub-criteria values (rows = sub-criteria, cols = alternatives)
    and a final row showing TOPSIS closeness per alternative.

    Accepts either:
      - the full `scores` dict your compute_topsis() returns (recommended), or
      - a pandas.DataFrame (score_matrix) and optionally a ranking_df.

    Expected DataFrame shape:
      - index = alternatives (e.g. "Bank Deposits")
      - columns = sub-criteria (e.g. "Availability", "Information", ...)
    """
    import pandas as pd
    import streamlit as st
    from results.constants import ALT_COLORS, ALTERNATIVES

    # --- normalize inputs ---
    score_matrix = None
    if isinstance(score_matrix_or_scores, dict):
        s = score_matrix_or_scores
        score_matrix = s.get("score_matrix")
        if score_matrix is None:
            # try to build from weighted_df (alternatives x subcriteria -> transpose)
            w = s.get("weighted_df")
            if isinstance(w, pd.DataFrame):
                # weighted_df in your outputs is subcriteria x alternatives; transpose if needed
                if (
                    list(w.index)
                    and list(w.columns)
                    and w.index.dtype == object
                    and w.columns.dtype == object
                ):
                    # detect orientation: if index are subcriteria and columns alternatives -> transpose
                    # prefer alternatives as index (makes iteration easier)
                    if all(alt in w.columns for alt in ALTERNATIVES):
                        score_matrix = w.transpose()
                    else:
                        score_matrix = w.copy()
                else:
                    score_matrix = w.copy()
        # pull ranking_df if present
        ranking_df = ranking_df or s.get("ranking_df")
    else:
        score_matrix = score_matrix_or_scores

    if score_matrix is None:
        st.error("No score matrix available to render heatmap.")
        return

    # ensure DataFrame
    if not isinstance(score_matrix, pd.DataFrame):
        score_matrix = pd.DataFrame(score_matrix)

    # Build header (alternatives)
    header_cells = "".join(
        f'<th style="color:{ALT_COLORS.get(a, "#333")};">{a}</th>' for a in ALTERNATIVES
    )

    # Build tbody: iterate over sub-criteria (columns)
    tbody = ""
    for sub in score_matrix.columns:
        # gather values in ALTERNATIVES order robustly
        vals = []
        for alt in ALTERNATIVES:
            try:
                if alt in score_matrix.index and sub in score_matrix.columns:
                    v = float(score_matrix.at[alt, sub])
                elif sub in score_matrix.index and alt in score_matrix.columns:
                    # fallback if orientation is flipped
                    v = float(score_matrix.at[sub, alt])
                else:
                    v = float("nan")
            except Exception:
                v = float("nan")
            vals.append(v)

        # numeric safety: ignore NaNs when computing min/max
        valid_vals = [v for v in vals if pd.notna(v)]
        if valid_vals:
            min_v, max_v = min(valid_vals), max(valid_vals)
        else:
            min_v, max_v = 0.0, 1.0

        tbody += f"<tr><td>{sub}</td>"
        for v in vals:
            if pd.isna(v):
                cell_txt = "&ndash;"
                alpha = 0.06
            else:
                # normalize so stronger = deeper color
                denom = (max_v - min_v) if (max_v - min_v) != 0 else 1.0
                norm = (v - min_v) / denom
                alpha = 0.06 + norm * 0.55
                cell_txt = f"{v:.3f}"
            bg = f"rgba(17,152,34,{alpha:.2f})"
            tbody += f'<td style="background:{bg};">{cell_txt}</td>'
        tbody += "</tr>"

    # Overall / closeness row
    # Prefer TOPSIS closeness (ranking_df["Closeness"]) if present; otherwise sum sub-criteria scores.
    closeness_map = {}
    if (
        isinstance(ranking_df, pd.DataFrame)
        and "Alternative" in ranking_df.columns
        and "Closeness" in ranking_df.columns
    ):
        closeness_map = dict(zip(ranking_df["Alternative"], ranking_df["Closeness"]))
    else:
        # fallback: sum sub-criteria values per alternative (normalize afterwards)
        try:
            sum_series = score_matrix.sum(axis=1)
            # normalize to [0,1] for display (if all zero, keep zeros)
            if (sum_series.max() - sum_series.min()) != 0:
                normed = (sum_series - sum_series.min()) / (
                    sum_series.max() - sum_series.min()
                )
                closeness_map = normed.to_dict()
            else:
                closeness_map = sum_series.to_dict()
        except Exception:
            closeness_map = {alt: 0.0 for alt in ALTERNATIVES}

    overall_row = '<tr class="overall-row"><td><b>TOPSIS closeness</b></td>'
    for alt in ALTERNATIVES:
        c = ALT_COLORS.get(alt, "#333")
        val = closeness_map.get(alt, 0.0)
        # If closeness is a raw sum fallback, we may want to format up to 4 decimals
        overall_row += f'<td style="color:{c};font-weight:700;">' f"{val:.5f}</td>"
    overall_row += "</tr>"

    st.markdown(
        f"""
<div class="heatmap-table-wrap">
<table class="heatmap-table">
  <thead><tr><th>Sub-criteria</th>{header_cells}</tr></thead>
  <tbody>{tbody}{overall_row}</tbody>
</table>
</div>
""",
        unsafe_allow_html=True,
    )
