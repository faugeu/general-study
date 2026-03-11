SAATY_OPTIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

TOOLTIPS = {
    "Availability": "Can be purchased or invested in easily",
    "Information": "Quality and transparency of data available about the option.",
    "Simplicity": "Full understanding of a financial product",
    "Stability": "Little or no danger of losing the investment",
    "Ability to save money": "Capacity to set aside money regularly",
    "Financial priorities": "Goals that guide where money is allocated",
    "Level of income": "Overall earnings that determine saving potential",
    "Liquidity": "The ability to quickly convert the investment into cash",
    "Return": "Dividends or interest to spend and/or reinvest",
    "Success rate": "Likelihood of achieving the target return",
    "Volatility": "The level of risk associated with price changes",
    "Experience": "Prior hands-on engagement with financial instruments",
    "Financial education": "Knowledge of finance, investing, and economics",
    "Risk attitude": "Tolerance for uncertainty and potential losses",
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
        "key": "fin_sec",
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
        "key": "personal",
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
        "key": "profit",
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
