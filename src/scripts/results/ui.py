"""results/ui.py — CSS injection and shared UI render helpers."""

import streamlit as st

from results.charts import fmt
from results.constants import ALT_COLORS, ALTERNATIVES

_CSS = """
<style>
.params-bar {
    display: flex; gap: 24px; flex-wrap: wrap;
    background: #f7f9f7; border: 1px solid #d6ead7;
    border-radius: 10px; padding: 16px 24px; margin-bottom: 24px;
}
.params-item { display: flex; flex-direction: column; gap: 4px; }
.params-lbl {
    font-size: 12px; color: #000; letter-spacing: 1px;
    text-transform: uppercase; font-weight: 500;
}
.params-val { font-size: 16px; font-weight: 600; color: #119822; }
.crit-card {
    background: #fafbfa; border: 1px solid #e2e8e2;
    border-radius: 10px; padding: 16px 20px; margin-bottom: 10px;
}
.crit-head { display: flex; align-items: center; gap: 12px; }
.crit-dot  { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.crit-name { font-size: 16px; font-weight: 700; color: #000; flex: 1; }
.crit-pct  { font-size: 20px; font-weight: 700; }
.mini-bar-wrap {
    width: 70px; height: 6px; background: rgba(0,0,0,0.07);
    border-radius: 99px; overflow: hidden; margin-left: 8px;
}
.mini-bar-fill { height: 100%; border-radius: 99px; }
.sub-row { display: flex; align-items: center; gap: 12px; margin-top: 12px; }
.sub-name { font-size: 13px; color: #000; width: 160px; flex-shrink: 0; }
.sub-bar-wrap {
    flex: 1; height: 6px; background: rgba(0,0,0,0.06);
    border-radius: 99px; overflow: hidden;
}
.sub-bar-fill { height: 100%; border-radius: 99px; opacity: 0.8; }
.sub-val { font-size: 13px; color: #000; width: 52px; text-align: right; }
.heatmap-table-wrap { overflow-x: auto; }
.heatmap-table {
    width: 100%; border-collapse: collapse; font-size: 14px;
}
.heatmap-table th {
    padding: 10px 14px; color: #000; font-weight: 600; font-size: 13px;
    border-bottom: 1px solid #e0e0e0; text-align: center; white-space: nowrap;
}
.heatmap-table th:first-child { text-align: left; }
.heatmap-table td {
    padding: 9px 14px; text-align: center;
    font-size: 13px; white-space: nowrap; border-bottom: 1px solid #f0f0f0;
}
.heatmap-table td:first-child { text-align: left; color: #000; }
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
    section_header("Final Ranking")

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
            f'<div style="font-size:14px;color:#000;margin-bottom:6px;'
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
                f'<div style="flex:1;background:#f5f5f5;'
                f"border:1px solid #e0e0e0;border-radius:8px;"
                f'padding:14px 16px;text-align:center;">'
                f'<div style="font-size:12px;color:#000;margin-bottom:4px;">'
                f"#{rank_n}</div>"
                f'<div style="font-size:15px;color:#000;font-weight:500;">'
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
    p50 = float(np.percentile(finals, 50))
    p90 = float(np.percentile(finals, 90))
    success_pct = float((finals >= goal).sum() / n * 100) if goal > 0 else 0.0

    m1, m2, m3 = st.columns(3)
    m1.metric("Median Terminal Wealth", f"{fmt(p50)} USD")
    m2.metric("P90 Terminal Wealth", f"{fmt(p90)} USD")
    m3.metric("Probability >= Goal", f"{success_pct:.1f}%")

    st.markdown(
        f'<div style="font-size:14px;font-weight:600;color:{color};'
        f'margin:12px 0 4px;">Simulation Run Chart</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        build_run_chart(result, alt, time_horizon, goal),
        use_container_width=True,
        key=f"rc_{alt}",
    )

    st.markdown(
        f'<div style="font-size:14px;font-weight:600;color:{color};'
        f'margin:12px 0 4px;">Terminal Wealth Distribution</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        build_histogram(result, alt, goal),
        use_container_width=True,
        key=f"hc_{alt}",
    )


def render_ahp_criteria_cards(
    main_weights: dict[str, float],
    subs_by_parent: dict[str, list[tuple[str, float]]],
) -> None:
    from results.constants import CRIT_COLORS

    crit_display = {
        "Financial security": "Financial Security",
        "Personal characteristics": "Personal Characteristics",
        "Profitability": "Profitability",
        "Readiness": "Readiness",
    }
    sorted_main = sorted(main_weights.items(), key=lambda x: x[1], reverse=True)

    for raw_name, weight in sorted_main:
        display_name = crit_display.get(raw_name, raw_name)
        color = CRIT_COLORS.get(display_name, "#119822")
        pct = weight * 100
        bar_w = int(pct)
        sub_rows_html = "".join(
            f'<div class="sub-row">'
            f'<div class="sub-name">{name}</div>'
            f'<div class="sub-bar-wrap">'
            f'<div class="sub-bar-fill" style="width:{int(lw * 100)}%;'
            f'background:{color};"></div></div>'
            f'<div class="sub-val">{lw:.4f}</div>'
            f"</div>"
            for name, lw in sorted(
                subs_by_parent.get(display_name, []),
                key=lambda x: x[1],
                reverse=True,
            )
        )

        st.markdown(
            f"""
<div class="crit-card">
  <div class="crit-head">
    <div class="crit-dot" style="background:{color};"></div>
    <div class="crit-name">{display_name}
    </div>
    <div class="crit-pct" style="color:{color};">{pct:.1f}%</div>
    <div class="mini-bar-wrap">
      <div class="mini-bar-fill" style="width:{bar_w}%;background:{color};">
      </div>
    </div>
  </div>
  {sub_rows_html}
</div>
""",
            unsafe_allow_html=True,
        )


def render_ahp_heatmap(overall_scores: dict[str, float]) -> None:
    from results.constants import ALT_SUBSCORES

    header_cells = "".join(
        f'<th style="color:{ALT_COLORS[a]};">{a}</th>' for a in ALTERNATIVES
    )
    tbody = ""
    for sub, vals in ALT_SUBSCORES.items():
        min_v, max_v = min(vals), max(vals)
        tbody += f"<tr><td>{sub}</td>"
        for v in vals:
            norm = (v - min_v) / (max_v - min_v + 1e-9)
            alpha = 0.06 + norm * 0.55
            bg = f"rgba(17,152,34,{alpha:.2f})"
            tbody += f'<td style="background:{bg};">{v:.3f}</td>'
        tbody += "</tr>"

    overall_row = '<tr class="overall-row"><td><b>Overall priority</b></td>'
    for alt in ALTERNATIVES:
        c = ALT_COLORS.get(alt, "#333")
        overall_row += (
            f'<td style="color:{c};font-weight:700;">'
            f"{overall_scores.get(alt, 0):.5f}</td>"
        )
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
