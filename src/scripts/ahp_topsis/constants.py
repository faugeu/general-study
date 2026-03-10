"""Constants and decision matrix for AHP-TOPSIS investment analysis."""

import pandas as pd

ALTERNATIVES = [
    "Bank deposits",
    "Life insurance",
    "Mutual funds",
    "Real estate and commodities",
    "Stocks",
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
    "Availability": [0.36331, 0.12011, 0.36331, 0.09782, 0.05546],
    "Information": [0.11531, 0.34887, 0.34887, 0.13938, 0.04758],
    "Simplicity": [0.39135, 0.07098, 0.22831, 0.26013, 0.04924],
    "Stability": [0.17345, 0.19643, 0.06535, 0.53112, 0.03365],
    "Ability to save money": [0.26868, 0.46974, 0.06832, 0.14536, 0.04791],
    "Financial priorities": [0.15393, 0.13340, 0.26002, 0.38916, 0.06349],
    "Level of income": [0.19005, 0.31085, 0.31126, 0.09253, 0.09532],
    "Liquidity": [0.36957, 0.05992, 0.12822, 0.13559, 0.30670],
    "Return": [0.08883, 0.22863, 0.30442, 0.07906, 0.29906],
    "Volatility": [0.14220, 0.10566, 0.25502, 0.45483, 0.04229],
    "Experience": [0.43444, 0.07786, 0.19103, 0.25529, 0.04139],
    "Financial education": [0.37036, 0.05936, 0.21534, 0.29752, 0.05743],
    "Risk attitude": [0.17382, 0.08846, 0.15997, 0.53621, 0.04154],
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
