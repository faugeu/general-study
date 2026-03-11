"""
results/page.py
===============
Entry point for Page 2 — Results.

Usage in the main app:

    from results.page import render_results_page

    elif st.session_state.page == 2:
        render_results_page()
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
    """
    Read a user-entered value from session_state.
    Raises a clear error if the key is missing so silent fallbacks
    to hardcoded defaults never hide a missing-data bug.
    """
    if key in st.session_state:
        return st.session_state[key]
    return default


def _mc_params_changed(current: dict) -> bool:
    """Return True if Monte Carlo input parameters differ from the last run."""
    snapshot = st.session_state.get(_MC_PARAMS_KEY)
    return snapshot != current


def render_results_page() -> None:
    """Render all three sections of the Results page."""
    inject_css()

    if "ahp_matrices" not in st.session_state:
        st.warning("No survey data found. Please complete the survey first.")
        return

    # ── Pull session values saved by savings/page.py ─────────────
    # All five fields are written to session_state by st.number_input
    # (via key=) and explicitly re-saved on "NEXT →" click, so they
    # are guaranteed to reflect the latest user inputs.
    matrices = st.session_state["ahp_matrices"]
    # Read from "profile_*" keys written by savings/page.py on "NEXT →" click.
    # These are separate from the widget keys (savings_target, time_horizon …)
    # to avoid StreamlitAPIException on active widget keys.
    savings_target = _get_session_value("profile_savings_target", 100_000_000)
    time_horizon = _get_session_value("profile_time_horizon", 6)
    monthly_income = _get_session_value("profile_monthly_income", 20_000_000)
    monthly_spending = _get_session_value("profile_monthly_spending", 9_000_000)
    initial_wealth = _get_session_value("profile_initial_wealth", 50_000_000)
    monthly_savings = max(0.0, monthly_income - monthly_spending)

    # ── Compute AHP weights (fast, no cache needed) ───────────────
    main_weights, sub_weights, subs_by_parent = compute_criteria_weights(matrices)
    scores = compute_topsis(sub_weights)

    # ── Params summary bar ────────────────────────────────────────
    render_params_bar(
        savings_target,
        time_horizon,
        monthly_income,
        monthly_spending,
        initial_wealth,
    )

    # ════════════════════════════════════════════════════════════
    # SECTION 1 — Final Ranking
    # ════════════════════════════════════════════════════════════
    render_final_ranking(scores)
    st.divider()

    # ════════════════════════════════════════════════════════════
    # SECTION 2 — Monte Carlo Simulation
    # ════════════════════════════════════════════════════════════
    section_header("Monte Carlo Simulation")
    st.markdown(
        f'<div style="font-size:14px;color:#000;margin-bottom:12px;">'
        f"1,000 trials per alternative · "
        f"Portfolio value over {time_horizon} months</div>",
        unsafe_allow_html=True,
    )

    # Build a snapshot of all parameters that affect the simulation.
    # If any of them changed since the last run, invalidate the cache
    # so results always reflect the current user inputs.
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
        # Save snapshot so we can detect future changes
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
        '<div style="font-size:14px;color:#000;margin-bottom:12px;">'
        "Criteria weights derived from your pairwise survey · "
        "Sub-criteria scores per alternative</div>",
        unsafe_allow_html=True,
    )

    render_ahp_criteria_cards(main_weights, subs_by_parent)

    st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:25px;font-weight:600;color:#000;'
        'margin-bottom:4px;">Sub-criteria Score Matrix</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:14px;color:#000;margin-bottom:12px;">'
        "Warmer cells = higher score within each row</div>",
        unsafe_allow_html=True,
    )
    render_ahp_heatmap(scores)
