import streamlit as st


def validate(values: dict) -> bool:
    """
    Display warnings for invalid inputs.
    Returns True if there is any blocking error (i.e. the Next button should be disabled).
    """
    zero_fields = {
        "savings_target": "Savings Target",
        "time_horizon": "Time Horizon",
        "monthly_income": "Monthly Income",
        "monthly_spending": "Monthly Spending",
        "initial_wealth": "Initial Wealth",
    }

    has_error = False

    for key, label in zero_fields.items():
        if values[key] == 0:
            st.warning(f"{label} cannot be 0.")
            has_error = True

    if values["monthly_spending"] >= values["monthly_income"]:
        st.warning("Monthly Spending should be less than Monthly Income.")
        # Not a hard block (fields are non-zero), but flag it
        has_error = True

    return has_error
