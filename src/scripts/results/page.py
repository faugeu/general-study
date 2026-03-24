"""
results/page.py
===============
Entry point for Page 2 — Results.
"""

import streamlit as st

from results.ahp import compute_criteria_weights, compute_topsis
from results.constants import ALTERNATIVES
from results.monte_carlo import run_all_simulations
from results.ui import (
    inject_css,
    render_ahp_criteria_cards,
    render_ahp_heatmap,
    render_final_ranking,
    render_monte_carlo_tab,
    render_params_bar,
    section_header,
)

_MC_CACHE_KEY = "mc_results"
_MC_PARAMS_KEY = "mc_params_snapshot"


def _get_session_value(key: str, default):
    if key in st.session_state:
        return st.session_state[key]
    return default


def _mc_params_changed(current: dict) -> bool:
    snapshot = st.session_state.get(_MC_PARAMS_KEY)
    return snapshot != current


def render_results_page() -> None:
    """Render all three sections of the Results page."""
    inject_css()

    if "ahp_matrices" not in st.session_state:
        st.warning("No survey data found. Please complete the survey first.")
        return

    # ── Example mode banner ───────────────────────────────────────
    if st.session_state.get("is_example"):
        st.markdown(
            '<div style="'
            "background:rgba(17,152,34,0.12);"
            "border:1px solid #119822;"
            "border-radius:8px;"
            "padding:12px 18px;"
            "margin-bottom:18px;"
            "font-size:13px;"
            'color:var(--text-color);">'
            "<b>Example Mode</b> — You are viewing a sample result for "
            "<b>Minh, 27 y/o</b>, an office worker saving toward "
            "<b>$8,000 USD</b> over <b>18 months</b> "
            "(income $700 · spending $420 · initial wealth $1,200). "
            "His survey reflects a preference for <b>Profitability</b> "
            "above all other criteria. "
            "Click <b>Savings Profile</b> above to enter your own data."
            "</div>",
            unsafe_allow_html=True,
        )

    # ── Pull session values ───────────────────────────────────────
    matrices = st.session_state["ahp_matrices"]
    savings_target = _get_session_value("profile_savings_target", 100_000_000)
    time_horizon = _get_session_value("profile_time_horizon", 6)
    monthly_income = _get_session_value("profile_monthly_income", 20_000_000)
    monthly_spending = _get_session_value("profile_monthly_spending", 9_000_000)
    initial_wealth = _get_session_value("profile_initial_wealth", 50_000_000)
    monthly_savings = max(0.0, monthly_income - monthly_spending)

    # ── AHP weights ───────────────────────────────────────────────
    main_weights, sub_weights, subs_by_parent = compute_criteria_weights(matrices)
    scores = compute_topsis(sub_weights)

    # ── Params bar ────────────────────────────────────────────────
    render_params_bar(
        savings_target,
        time_horizon,
        monthly_income,
        monthly_spending,
        initial_wealth,
    )

    # ── Explanation box helper ──────────────────────────────────────
    def _info_box(text: str) -> None:
        st.markdown(
            '<div style="'
            "background:rgba(17,152,34,0.08);"
            "border-left:3px solid #119822;"
            "border-radius:0 6px 6px 0;"
            "padding:10px 16px;"
            "margin-bottom:14px;"
            "font-size:13px;"
            "line-height:1.6;"
            'color:var(--text-color);opacity:0.85;">' + text + "</div>",
            unsafe_allow_html=True,
        )

    # ════════════════════════════════════════════════════════════
    # SECTION 1 — Final Ranking
    # ════════════════════════════════════════════════════════════
    section_header("Final Ranking")

    _info_box(
        "The <b>Final Ranking</b> combines your AHP criteria weights with TOPSIS scores "
        "to produce an overall recommendation that best matches "
        "your financial profile and stated priorities. "
        "Higher score = the option is closer to the ideal solution "
    )
    render_final_ranking(scores)
    st.divider()

    # ════════════════════════════════════════════════════════════
    # SECTION 2 — Monte Carlo Simulation
    # ════════════════════════════════════════════════════════════

    section_header("Monte Carlo Simulation")
    st.markdown(
        f'<div style="font-size:14px;color:var(--text-color);'
        f'opacity:0.75;margin-bottom:12px;">'
        f"1,000 trials per alternative · "
        f"Portfolio value over {time_horizon} months</div>",
        unsafe_allow_html=True,
    )

    _info_box(
        "The <b>Monte Carlo Simulation</b> runs 1,000 random scenarios for each saving "
        "to estimate outcome ranges and the probability of reaching your savings goal. "
    )

    mc_params = {
        "time_horizon": time_horizon,
        "monthly_savings": monthly_savings,
        "initial_wealth": initial_wealth,
    }

    if _mc_params_changed(mc_params):
        st.session_state.pop(_MC_CACHE_KEY, None)

    if _MC_CACHE_KEY not in st.session_state:
        with st.spinner("Running Monte Carlo simulations…"):
            st.session_state[_MC_CACHE_KEY] = run_all_simulations(
                time_horizon=time_horizon,
                monthly_savings=monthly_savings,
                initial_wealth=initial_wealth,
            )
        st.session_state[_MC_PARAMS_KEY] = mc_params

    mc = st.session_state[_MC_CACHE_KEY]
    tabs = st.tabs(ALTERNATIVES)
    for tab, alt in zip(tabs, ALTERNATIVES):
        with tab:
            render_monte_carlo_tab(
                alt=alt,
                result=mc[alt],
                goal=savings_target,
                time_horizon=time_horizon,
            )

    st.divider()

    # ════════════════════════════════════════════════════════════
    # SECTION 3 — AHP Decision Framework
    # ════════════════════════════════════════════════════════════

    section_header("AHP Decision Framework")
    st.markdown(
        '<div style="font-size:14px;color:var(--text-color);'
        'opacity:0.75;margin-bottom:12px;">'
        "Criteria weights derived from your pairwise survey · "
        "Sub-criteria scores per alternative</div>",
        unsafe_allow_html=True,
    )

    _info_box(
        "The <b>AHP</b> assigns weights to criteria based on your pairwise comparisons"
        ", showing how strongly each factor influences the final decision. "
    )
    render_ahp_criteria_cards(main_weights, subs_by_parent)

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:25px;font-weight:600;color:var(--text-color);'
        'margin-bottom:4px;">Sub-criteria Score Matrix</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:14px;color:var(--text-color);'
        'opacity:0.75;margin-bottom:12px;">'
        "Warmer cells = higher score within each row</div>",
        unsafe_allow_html=True,
    )
    _info_box(
        "The <b>Sub-criteria Score Matrix</b> compares how each option "
        "performs on every sub-criterion, with color indicating "
        "strengths and weaknesses across dimensions. "
    )
    render_ahp_heatmap(scores)
