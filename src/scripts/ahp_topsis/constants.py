"""Constants and decision matrix for AHP-TOPSIS investment analysis."""

import pandas as pd

ALTERNATIVES = [
    "Bank Deposits",
    "Stocks",
    "Mutual Funds",
    "Real Estate & Commodities",
]

CRITERIA = [
    "Financial security",
    "Personal characteristics",
    "Profitability",
    "Readiness",
]

SUBCRITERIA = {
    "Financial security": [
        "Availability",
        "Information",
        "Simplicity",
        "Stability",
    ],
    "Personal characteristics": [
        "Ability to save money",
        "Financial priorities",
        "Level of income",
    ],
    "Profitability": [
        "Liquidity",
        "Return",
        "Volatility",
    ],
    "Readiness": [
        "Experience",
        "Financial education",
        "Risk attitude",
    ],
}

DECISION_MATRIX = {
    "Availability": [0.36331, 0.05546, 0.36331, 0.09782],
    "Information": [0.11531, 0.04758, 0.34887, 0.13938],
    "Simplicity": [0.39135, 0.04924, 0.22831, 0.26013],
    "Stability": [0.17345, 0.03365, 0.06535, 0.53112],
    "Ability to save money": [0.26868, 0.04791, 0.06832, 0.14536],
    "Financial priorities": [0.15393, 0.06349, 0.26002, 0.38916],
    "Level of income": [0.19005, 0.09532, 0.31126, 0.09253],
    "Liquidity": [0.36957, 0.30670, 0.12822, 0.13559],
    "Return": [0.08883, 0.29906, 0.30442, 0.07906],
    "Volatility": [0.14220, 0.04229, 0.25502, 0.45483],
    "Experience": [0.43444, 0.04139, 0.19103, 0.25529],
    "Financial education": [0.37036, 0.05743, 0.21534, 0.29752],
    "Risk attitude": [0.17382, 0.04154, 0.15997, 0.53621],
}

CRITERION_TYPES = {
    "Availability": "benefit",
    "Information": "benefit",
    "Simplicity": "benefit",
    "Stability": "benefit",
    "Ability to save money": "benefit",
    "Financial priorities": "benefit",
    "Level of income": "benefit",
    "Liquidity": "benefit",
    "Return": "benefit",
    "Volatility": "cost",
    "Experience": "benefit",
    "Financial education": "benefit",
    "Risk attitude": "benefit",
}


def get_decision_df():
    """Decision matrix as DataFrame (subcriteria x alternatives)."""
    return pd.DataFrame(DECISION_MATRIX, index=ALTERNATIVES).T
