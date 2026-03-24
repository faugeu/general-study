"""results/constants.py — Shared constants for the Results page."""

ALTERNATIVES = [
    "Bank Deposits",
    "Stocks",
    "Mutual Funds",
    "Real Estate & Commodities",
]

ALT_COLORS: dict[str, str] = {
    "Bank Deposits": "#21A84A",
    "Stocks": "#2680EB",
    "Mutual Funds": "#c9a96e",
    "Real Estate & Commodities": "#de6eae",
}

# Annual return / annual volatility per alternative
ALT_PARAMS: dict[str, dict[str, float]] = {
    "Bank Deposits": {"r": 0.055, "v": 0.01},
    "Stocks": {"r": 0.15, "v": 0.22},
    "Mutual Funds": {"r": 0.09, "v": 0.10},
    "Real Estate & Commodities": {"r": 0.10, "v": 0.14},
}

# # Fixed AHP reference scores: sub-criterion → [score per alternative]
# ALT_SUBSCORES: dict[str, list[float]] = {
#     "Availability": [0.363, 0.120, 0.363, 0.098],
#     "Information": [0.115, 0.139, 0.349, 0.139],
#     "Simplicity": [0.391, 0.260, 0.228, 0.260],
#     "Stability": [0.173, 0.065, 0.065, 0.531],
#     "Ability to save": [0.269, 0.145, 0.068, 0.145],
#     "Financial priorities": [0.154, 0.389, 0.260, 0.389],
#     "Level of income": [0.190, 0.093, 0.311, 0.093],
#     "Liquidity": [0.370, 0.136, 0.128, 0.136],
#     "Return": [0.089, 0.079, 0.304, 0.079],
#     "Volatility": [0.142, 0.455, 0.255, 0.455],
#     "Success Rate": [0.000, 0.000, 0.000, 0.000],
#     "Experience": [0.434, 0.255, 0.191, 0.255],
#     "Financial education": [0.370, 0.298, 0.215, 0.298],
#     "Risk attitude": [0.174, 0.536, 0.160, 0.536],
# }

CRIT_COLORS: dict[str, str] = {
    "Financial Security": "#c9a96e",
    "Personal Characteristics": "#de6eae",
    "Profitability": "#6edfc9",
    "Readiness": "#5b8dee",
}

# Maps AHP matrix key → display label
CRIT_KEY_LABEL: dict[str, str] = {
    "financial security": "Financial Security",
    "personal": "Personal Characteristics",
    "profit": "Profitability",
    "readiness": "Readiness",
}

# Maps raw survey criterion name → display label + matrix key
CRIT_RAW_MAP: dict[str, tuple[str, str]] = {
    "Financial security": ("financial security", "Financial Security"),
    "Personal characteristics": ("personal", "Personal Characteristics"),
    "Profitability": ("profit", "Profitability"),
    "Readiness": ("readiness", "Readiness"),
}

N_SIMS = 1000
