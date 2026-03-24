# results/page.py
"""
results/page.py
===============
Entry point for Page 2 — Results.

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


def _interpret_ahp_weights(main_weights: dict, subs_by_parent: dict) -> str:
    """Generate human-readable insights from AHP weights (tailored for example mode)."""

    # Sort main criteria
    sorted_main = sorted(main_weights.items(), key=lambda x: x[1], reverse=True)

    top_main, top_val = sorted_main[0]
    second_main, second_val = sorted_main[1]

    # Get top sub-criteria per main
    sub_insights = []
    for parent, subs in subs_by_parent.items():
        if not subs:
            continue
        top_sub = max(subs.items(), key=lambda x: x[1])
        sub_insights.append(f"<b>{parent}</b>: {top_sub[0]}")

    sub_text = " · ".join(sub_insights)

    return (
        f"For this profile, <b>{top_main}</b> is the dominant decision driver, "
        f"indicating a strong preference toward outcomes related to this dimension. "
        f"<b>{second_main}</b> is also important but plays a secondary role.\n\n"
        f"At a more detailed level, key priorities include: {sub_text}. "
        f"This suggests the decision is primarily influenced by these specific factors."
    )


def _get_session_value(key: str, default):
    """Read a user-entered value from session_state or return default."""
    return st.session_state.get(key, default)


def _mc_params_changed(current: dict) -> bool:
    snapshot = st.session_state.get(_MC_PARAMS_KEY)
    return snapshot != current


def render_results_page() -> None:
    """Render the Results page: run MC, merge MC rows into decision matrix, run AHP+TOPSIS, render UI."""
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
    monthly_savings = _get_session_value(
        "profile_monthly_savings", monthly_income - monthly_spending
    )
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

    # Optional: In topsis code already has a normalization step
    # for name in mc_rows.keys():
    #     merged_df.loc[name] = _vector_normalize_row(merged_df.loc[name].values.tolist())

    # --- Compute AHP weights and run TOPSIS using the merged decision matrix ---
    main_weights, sub_weights, subs_by_parent = compute_criteria_weights(matrices)
    scores = compute_topsis(sub_weights, decision_df_override=merged_df)

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
        f'<div style="font-size:14px;color:var(--text-color);'
        f'opacity:0.75;margin-bottom:12px;">'
        f"1,000 trials per alternative · "
        f"Savings over {time_horizon} months</div>",
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
                initial_wealth=initial_wealth,
                monthly_income=monthly_income,
                monthly_spending=monthly_spending,
            )
        st.session_state[_MC_PARAMS_KEY] = mc_params

    mc = st.session_state[_MC_CACHE_KEY]
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

    if st.session_state.get("is_example"):
        _info_box(
            "<b>Minh’s Decision Profile</b><br><br>"
            + _interpret_ahp_weights(main_weights, subs_by_parent)
        )
    else:
        _info_box(
            "The <b>AHP</b> assigns weights to criteria based on your pairwise comparisons, "
            "showing how strongly each factor influences the final decision."
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
