# results/page.py
"""
results/page.py
===============
Entry point for Page 2 — Results.

Usage in the main app:

    from results.page import render_results_page

    elif st.session_state.page == 2:
        render_results_page()
"""
from typing import Dict, List, Optional
import pandas as pd
import streamlit as st

from ahp_topsis.constants import get_decision_df
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
    """Read a user-entered value from session_state or return default."""
    return st.session_state.get(key, default)


def _mc_params_changed(current: dict) -> bool:
    """Return True if Monte Carlo input parameters differ from the last run."""
    snapshot = st.session_state.get(_MC_PARAMS_KEY)
    return snapshot != current


def render_results_page() -> None:
    """Render the Results page: run MC, merge MC rows into decision matrix, run AHP+TOPSIS, render UI."""
    inject_css()

    if "ahp_matrices" not in st.session_state:
        st.warning("No survey data found. Please complete the survey first.")
        return

    # --- load session inputs (written by savings/page.py) ---
    matrices = st.session_state["ahp_matrices"]
    savings_target = _get_session_value("profile_savings_target", 100_000_000)
    time_horizon = _get_session_value("profile_time_horizon", 6)
    monthly_income = _get_session_value("profile_monthly_income", 20_000_000)
    monthly_spending = _get_session_value("profile_monthly_spending", 9_000_000)
    initial_wealth = _get_session_value("profile_initial_wealth", 50_000_000)

    # --- Monte Carlo: run (or load cached) before TOPSIS so MC rows are incorporated ---
    mc_params = {
        "time_horizon": time_horizon,
        "initial_wealth": initial_wealth,
        "monthly_income": monthly_income,
        "monthly_spending": monthly_spending,
    }

    if _mc_params_changed(mc_params):
        st.session_state.pop(_MC_CACHE_KEY, None)

    if _MC_CACHE_KEY not in st.session_state:
        with st.spinner("Running Monte Carlo simulations…"):
            st.session_state[_MC_CACHE_KEY] = run_all_simulations(
                time_horizon=time_horizon,
                initial_wealth=initial_wealth,
                monthly_income=monthly_income,
                monthly_spending=monthly_spending,
            )
        st.session_state[_MC_PARAMS_KEY] = mc_params

    mc = st.session_state[_MC_CACHE_KEY]

    def _vector_normalize_row(vals: List[float]) -> List[float]:
        """Return a vector-normalized copy of vals (Euclidean norm)."""
        s = pd.Series(vals, dtype=float)
        denom = (s**2).sum() ** 0.5
        if denom == 0:
            return [0.0] * len(vals)
        return (s / denom).tolist()

    # --- compute MC-derived rows per alternative ---
    mc_return_p50: Dict[str, float] = {}
    mc_volatility: Dict[str, float] = {}
    mc_success_rate: Dict[str, float] = {}

    for alt in ALTERNATIVES:
        alt_res = mc.get(alt, {})
        final_vals = alt_res["finals"]

        if len(final_vals) == 0:
            mc_return_p50[alt] = 0.0
            mc_volatility[alt] = 0.0
            mc_success_rate[alt] = 0.0
            continue

        arr = pd.Series(final_vals).astype(float)
        mc_return_p50[alt] = float(arr.quantile(0.5))  # median final value
        mc_volatility[alt] = float(arr.std(ddof=1))  # sample standard deviation
        mc_success_rate[alt] = float(
            (arr >= savings_target).mean()
        )  # fraction meeting target

    # after computing all alternatives
    if all(v == 0 for v in mc_success_rate.values()):
        n = len(mc_success_rate)
        mc_success_rate = {k: 1 / n for k in mc_success_rate}

    # --- load base decision matrix and merge MC rows ---
    base_decision_df = get_decision_df()  # index=subcriteria, columns=alternatives
    merged_df = base_decision_df.copy()
    merged_df = merged_df.reindex(columns=ALTERNATIVES)  # enforce column order

    mc_rows = {
        "Return": [mc_return_p50.get(alt, 0.0) for alt in ALTERNATIVES],
        "Volatility": [mc_volatility.get(alt, 0.0) for alt in ALTERNATIVES],
        "Success rate": [mc_success_rate.get(alt, 0.0) for alt in ALTERNATIVES],
    }

    for row_name, values in mc_rows.items():
        merged_df.loc[row_name] = values

    print("Merged decision matrix with MC rows:", merged_df)

    for name in mc_rows.keys():
        merged_df.loc[name] = _vector_normalize_row(merged_df.loc[name].values.tolist())

    # --- Compute AHP weights and run TOPSIS using the merged decision matrix ---
    main_weights, sub_weights, subs_by_parent = compute_criteria_weights(matrices)
    scores = compute_topsis(sub_weights, decision_df_override=merged_df)

    # --- Render parameter summary ---
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
    ranking_df = scores.get("ranking_df")
    ranking_dict = {}
    if (
        ranking_df is not None
        and "Alternative" in ranking_df.columns
        and "Closeness" in ranking_df.columns
    ):
        ranking_dict = dict(zip(ranking_df["Alternative"], ranking_df["Closeness"]))
    else:
        # fallback: try to build ranking dict from topsis_result if present
        topsis_result = scores.get("topsis_result", {})
        if isinstance(topsis_result, dict) and "ranking_df" in topsis_result:
            rdf = topsis_result["ranking_df"]
            if (
                isinstance(rdf, pd.DataFrame)
                and "Alternative" in rdf.columns
                and "Closeness" in rdf.columns
            ):
                ranking_dict = dict(zip(rdf["Alternative"], rdf["Closeness"]))

    render_final_ranking(ranking_dict)
    st.divider()

    # ════════════════════════════════════════════════════════════
    # SECTION 2 — Monte Carlo Simulation (tabs)
    # ════════════════════════════════════════════════════════════
    section_header("Monte Carlo Simulation")
    st.markdown(
        f'<div style="font-size:14px;color:#000;margin-bottom:12px;">'
        f"1,000 trials per alternative · "
        f"Portfolio value over {time_horizon} months</div>",
        unsafe_allow_html=True,
    )

    tabs = st.tabs(ALTERNATIVES)
    for tab, alt in zip(tabs, ALTERNATIVES):
        with tab:
            render_monte_carlo_tab(
                alt=alt,
                result=mc.get(alt, {}),
                goal=savings_target,
                time_horizon=time_horizon,
            )

    st.divider()

    # ════════════════════════════════════════════════════
    # SECTION 3 — AHP Decision Framework (cards + heatmap)
    # ════════════════════════════════════════════════════
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

    # render heatmap: pass the full scores dict (function extracts score_matrix + ranking_df)
    render_ahp_heatmap(scores)
