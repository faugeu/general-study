SAATY_OPTIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

TOOLTIPS = {
    "Availability": "Can be purchased or invested in easily",
    "Information": "Quality, transparency, and timeliness of data available about the option",
    "Simplicity": "Degree to which a financial product is fully understandable",
    "Stability": "Investment has little or no risk of capital loss",
    "Ability to save money": "Capacity to regularly set aside money",
    "Financial priorities": "Goals that guide allocation of financial resources",
    "Level of income": "Total earnings that determine the potential to save and invest",
    "Liquidity": "Ability to quickly convert the investment into cash without significant loss",
    "Return": "Expected median return (p50) from dividends or interest to spend and/or reinvest",
    "Success rate": "Probability of achieving the target return",
    "Volatility": "Measured standard deviation of returns, indicating the level of price risk",
    "Experience": "Prior hands-on engagement with financial instruments",
    "Financial education": "Knowledge of finance, investing, and economic concepts",
    "Risk attitude": "Individual tolerance for uncertainty and potential financial losses",
}

MATRICES = [
    {
        "key": "main",
        "title": "Matrix 1: Main Criterias",
        "criteria": [
            "Financial security",
            "Personal characteristics",
            "Profitability",
            "Readiness",
        ],
        "pairs": [
            ("Financial security", "Personal characteristics"),
            ("Financial security", "Profitability"),
            ("Financial security", "Readiness"),
            ("Personal characteristics", "Profitability"),
            ("Personal characteristics", "Readiness"),
            ("Profitability", "Readiness"),
        ],
    },
    {
        "key": "financial security",
        "title": 'Matrix 2: Sub-criteria — "Financial Security"',
        "criteria": ["Availability", "Information", "Simplicity", "Stability"],
        "pairs": [
            ("Availability", "Information"),
            ("Availability", "Simplicity"),
            ("Availability", "Stability"),
            ("Information", "Simplicity"),
            ("Information", "Stability"),
            ("Simplicity", "Stability"),
        ],
    },
    {
        "key": "personal characteristics",
        "title": 'Matrix 3: Sub-criteria — "Personal Characteristics"',
        "criteria": [
            "Ability to save money",
            "Financial priorities",
            "Level of income",
        ],
        "pairs": [
            ("Ability to save money", "Financial priorities"),
            ("Ability to save money", "Level of income"),
            ("Financial priorities", "Level of income"),
        ],
    },
    {
        "key": "profitability",
        "title": 'Matrix 4: Sub-criteria — "Profitability"',
        "criteria": ["Liquidity", "Return", "Success rate", "Volatility"],
        "pairs": [
            ("Liquidity", "Return"),
            ("Liquidity", "Success rate"),
            ("Liquidity", "Volatility"),
            ("Return", "Success rate"),
            ("Return", "Volatility"),
            ("Success rate", "Volatility"),
        ],
    },
    {
        "key": "readiness",
        "title": 'Matrix 5: Sub-criteria — "Readiness"',
        "criteria": ["Experience", "Financial education", "Risk attitude"],
        "pairs": [
            ("Experience", "Financial education"),
            ("Experience", "Risk attitude"),
            ("Financial education", "Risk attitude"),
        ],
    },
]
