import streamlit as st
from .constants import FIELD_DEFAULTS, FIELD_STEPS, FIELD_LABELS


def render_inputs() -> dict:
    """Render all savings profile input fields and return their current values."""
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        savings_target = st.number_input(
            FIELD_LABELS["savings_target"],
            min_value=0,
            value=FIELD_DEFAULTS["savings_target"],
            step=FIELD_STEPS["savings_target"],
            key="savings_target",
        )
    with col_b:
        time_horizon = st.number_input(
            FIELD_LABELS["time_horizon"],
            min_value=0,
            value=FIELD_DEFAULTS["time_horizon"],
            step=FIELD_STEPS["time_horizon"],
            key="time_horizon",
        )
    with col_c:
        monthly_income = st.number_input(
            FIELD_LABELS["monthly_income"],
            min_value=0,
            value=FIELD_DEFAULTS["monthly_income"],
            step=FIELD_STEPS["monthly_income"],
            key="monthly_income",
        )

    col_d, col_e = st.columns(2)
    with col_d:
        monthly_spending = st.number_input(
            FIELD_LABELS["monthly_spending"],
            min_value=0,
            value=FIELD_DEFAULTS["monthly_spending"],
            step=FIELD_STEPS["monthly_spending"],
            key="monthly_spending",
        )
    with col_e:
        initial_wealth = st.number_input(
            FIELD_LABELS["initial_wealth"],
            min_value=0,
            value=FIELD_DEFAULTS["initial_wealth"],
            step=FIELD_STEPS["initial_wealth"],
            key="initial_wealth",
        )

    return {
        "savings_target": savings_target,
        "time_horizon": time_horizon,
        "monthly_income": monthly_income,
        "monthly_spending": monthly_spending,
        "initial_wealth": initial_wealth,
    }
