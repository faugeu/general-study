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

MATRIX_EXPLANATIONS = {
    "main": {
        "title": "Why these priorities?",
        "text": """
Minh places the highest importance on **Profitability**, reflecting his goal to grow limited savings efficiently within a short time horizon.

While **Financial Security** remains important, it is secondary to achieving higher returns. 
**Personal characteristics** and **Readiness** are considered less critical, as Minh is willing to adapt and learn while investing.

💡 *Insight:* This pattern is typical of early-career individuals aiming for faster capital growth despite moderate constraints.
""",
    },
    "financial security": {
        "title": "Focus on Stability",
        "text": """
Within financial security, Minh prioritizes **Stability** over availability or simplicity.

This suggests a preference for investments that are **predictable and less volatile**, even if they are slightly harder to access or understand.

💡 *Insight:* Despite being return-oriented, Minh still seeks a safety baseline to avoid major losses.
""",
    },
    "personal characteristics": {
        "title": "Income drives decisions",
        "text": """
Minh considers **Level of income** more important than saving ability or financial priorities.

This reflects the reality that his **limited income constrains how much he can save or invest**, making earning capacity the key factor.

💡 *Insight:* Financial decisions are strongly influenced by external constraints rather than personal preference alone.
""",
    },
    "profitability": {
        "title": "Return is king",
        "text": """
Minh strongly prioritizes **Return**, followed by liquidity and success rate, while placing less emphasis on volatility.

This indicates a willingness to **accept some risk in exchange for higher gains**, especially given his relatively small starting capital.

💡 *Insight:* This is a growth-oriented strategy, common for users aiming to accelerate wealth accumulation.
""",
    },
    "readiness": {
        "title": "Learning over experience",
        "text": """
Minh values **Financial education** more than experience or risk attitude.

This suggests he is still **building knowledge and confidence**, and relies more on learning than past investing experience.

💡 *Insight:* This profile fits a beginner investor who is open to guidance and gradual improvement.
""",
    },
}
