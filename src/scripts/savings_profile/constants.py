FIELD_DEFAULTS = {
    "savings_target": 1_000_000,
    "time_horizon": 24,
    "monthly_income": 20_000,
    "monthly_spending": 9_000,
    "initial_wealth": 50_000,
}

FIELD_STEPS = {
    "savings_target": 1_000,
    "time_horizon": 1,
    "monthly_income": 500,
    "monthly_spending": 500,
    "initial_wealth": 1_000,
}

FIELD_LABELS = {
    "savings_target": "Savings Target (USD)",
    "time_horizon": "Time Horizon (months)",
    "monthly_income": "Monthly Income - Net (USD)",
    "monthly_spending": "Monthly Spending (USD)",
    "initial_wealth": "Initial Wealth (USD)",
}
