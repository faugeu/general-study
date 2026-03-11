"""results/charts.py — Plotly chart builders for Monte Carlo results."""

import numpy as np
import plotly.graph_objects as go

from results.constants import ALT_COLORS, N_SIMS


def fmt(v: float) -> str:
    """Format a number into a compact USD string."""
    if v >= 1e9:
        return f"{v / 1e9:.1f}B"
    if v >= 1e6:
        return f"{v / 1e6:.1f}M"
    if v >= 1e3:
        return f"{v / 1e3:.0f}K"
    return f"{v:.0f}"


def _hex_dim(hex_color: str) -> str:
    """Return a darkened version of a hex color."""
    try:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"#{int(r*0.7):02x}{int(g*0.7):02x}{int(b*0.7):02x}"
    except Exception:
        return hex_color


def _hex_rgba(hex_color: str, alpha: float) -> str:
    try:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"rgba({r},{g},{b},{alpha})"
    except Exception:
        return f"rgba(100,100,100,{alpha})"


_LAYOUT_BASE: dict = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Outfit, sans-serif", "color": "#444"},
}


def build_run_chart(
    result: dict,
    alt_name: str,
    T: int,
    goal: float,
) -> go.Figure:
    """Monte Carlo run-chart: time × portfolio value."""
    color = ALT_COLORS[alt_name]
    dim = _hex_dim(color)
    band = _hex_rgba(color, 0.12)
    months = list(range(1, T + 1))

    fig = go.Figure()

    # Sample individual runs (performance)
    sample = result["runs"][:: max(1, N_SIMS // 60)]
    for run in sample:
        fig.add_trace(
            go.Scatter(
                x=months,
                y=run.tolist(),
                mode="lines",
                line={"color": "rgba(150,150,150,0.15)", "width": 0.6},
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # P10–P90 band
    fig.add_trace(
        go.Scatter(
            x=months + months[::-1],
            y=result["q90"].tolist() + result["q10"].tolist()[::-1],
            fill="toself",
            fillcolor=band,
            line={"width": 0},
            showlegend=False,
            hoverinfo="skip",
        )
    )

    # P10 / P90 dashed lines
    for key, label in [("q10", "P10"), ("q90", "P90")]:
        fig.add_trace(
            go.Scatter(
                x=months,
                y=result[key].tolist(),
                mode="lines",
                line={"color": dim, "width": 1.2, "dash": "dot"},
                name=label,
            )
        )

    # Median
    fig.add_trace(
        go.Scatter(
            x=months,
            y=result["median"].tolist(),
            mode="lines",
            line={"color": color, "width": 2.5},
            name="Median (P50)",
        )
    )

    min_mc = float(result["runs"].min())
    max_mc = float(result["runs"].max())
    y_bottom = min(min_mc, goal) if goal > 0 else min_mc
    y_top = max(max_mc, goal) if goal > 0 else max_mc
    y_pad = (y_top - y_bottom) * 0.05

    if goal > 0:
        fig.add_hline(
            y=goal,
            line_dash="dash",
            line_color="#e07b6e",
            line_width=1.4,
            annotation_text="Goal",
            annotation_font_color="#e07b6e",
            annotation_font_size=10,
        )

    fig.update_layout(
        **_LAYOUT_BASE,
        height=300,
        margin={"t": 10, "b": 40, "l": 60, "r": 20},
        xaxis={"title": "Month", "gridcolor": "rgba(0,0,0,0.06)"},
        yaxis={
            "title": "Portfolio Value (USD)",
            "gridcolor": "rgba(0,0,0,0.06)",
            "tickformat": ".3s",
            "range": [y_bottom - y_pad, y_top + y_pad],
        },
        legend={"orientation": "h", "y": -0.28, "x": 0, "font": {"size": 10}},
        hovermode="x unified",
    )
    return fig


def build_histogram(
    result: dict,
    alt_name: str,
    goal: float,
) -> go.Figure:
    """Terminal-wealth histogram with percentile markers."""
    color = ALT_COLORS[alt_name]
    dim = _hex_dim(color)
    finals = result["finals"]
    n = len(finals)

    p10 = float(np.percentile(finals, 10))
    p50 = float(np.percentile(finals, 50))
    p90 = float(np.percentile(finals, 90))
    success_pct = float((finals >= goal).sum() / n * 100) if goal > 0 else 0.0

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=finals.tolist(),
            nbinsx=40,
            marker_color=color,
            opacity=0.75,
            showlegend=False,
        )
    )

    for val, label, dash in [
        (p10, "P10", "dot"),
        (p50, "P50", "dash"),
        (p90, "P90", "longdash"),
    ]:
        fig.add_vline(
            x=val,
            line_dash=dash,
            line_color=dim,
            line_width=1.4,
            annotation_text=label,
            annotation_font_size=9,
            annotation_font_color=dim,
        )

    # goal line always shown regardless of whether it falls inside finals range
    if goal > 0:
        fig.add_vline(
            x=goal,
            line_dash="dash",
            line_color="#e07b6e",
            line_width=1.6,
            annotation_text="Goal",
            annotation_font_color="#e07b6e",
            annotation_font_size=9,
        )

    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0.99,
        y=0.97,
        xanchor="right",
        yanchor="top",
        text=(
            f"Median: <b>{fmt(p50)}</b>  "
            f"P90: <b>{fmt(p90)}</b>  "
            f"≥ Goal: <b>{success_pct:.1f}%</b>"
        ),
        showarrow=False,
        font={"size": 10, "color": "#555"},
        bgcolor="rgba(255,255,255,0.7)",
        bordercolor="rgba(0,0,0,0.08)",
        borderwidth=1,
        borderpad=4,
    )

    min_mc = float(finals.min())
    max_mc = float(finals.max())
    x_pad = (max_mc - min_mc) * 0.05
    # Only extend range toward goal if it is within 50% of the finals spread,
    # otherwise keep range tight on the data and let the goal line sit at edge.
    spread = max_mc - min_mc
    if goal > 0 and abs(goal - min_mc) <= spread * 1.5:
        x_left = min(min_mc, goal)
        x_right = max(max_mc, goal)
    else:
        x_left = min_mc
        x_right = max_mc
    nticks = 6

    fig.update_layout(
        **_LAYOUT_BASE,
        height=260,
        margin={"t": 10, "b": 50, "l": 50, "r": 10},
        xaxis={
            "title": "Terminal Wealth (USD)",
            "gridcolor": "rgba(0,0,0,0.06)",
            "tickformat": ".3s",
            "range": [x_left - x_pad, x_right + x_pad],
            "nticks": nticks,
        },
        yaxis={"title": "Frequency", "gridcolor": "rgba(0,0,0,0.06)"},
        bargap=0.04,
    )
    return fig
