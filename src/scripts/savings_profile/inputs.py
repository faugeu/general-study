import streamlit as st
from .constants import FIELD_DEFAULTS, FIELD_STEPS, FIELD_LABELS


def init_defaults():
    defaults = {
        "savings_target": 100_000,
        "monthly_income": 6_000,
        "time_horizon": 60,
        "monthly_spending": 4_000,
        "initial_wealth": 20_000,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_inputs() -> dict:
    init_defaults()

    col1, col2 = st.columns(2)

    with col1:
        savings_target = st.number_input(
            "Savings Target (USD)",
            min_value=0,
            step=1000,
            key="savings_target",
        )

        monthly_income = st.number_input(
            "Monthly Income (USD)",
            min_value=0,
            step=100,
            key="monthly_income",
        )

        time_horizon = st.number_input(
            "Time Horizon (months)",
            min_value=1,
            max_value=120,
            step=1,
            key="time_horizon",
        )

    with col2:
        monthly_spending = st.number_input(
            "Monthly Spending (USD)",
            min_value=0,
            step=100,
            key="monthly_spending",
        )

        initial_wealth = st.number_input(
            "Initial Wealth (USD)",
            min_value=0,
            step=1000,
            key="initial_wealth",
        )

    monthly_savings = monthly_income - monthly_spending

    return {
        "savings_target": savings_target,
        "time_horizon": time_horizon,
        "monthly_income": monthly_income,
        "monthly_spending": monthly_spending,
        "monthly_savings": monthly_savings,
        "initial_wealth": initial_wealth,
    }
