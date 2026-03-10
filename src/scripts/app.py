import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="OptimizeSaving", page_icon="💰", layout="wide")

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = 0  # 0 = Savings Profile, 1 = Survey, 2 = Results

# ---------- CSS ----------
# fmt: off
_CSS_LONG = (
    "div[data-testid='stNumberInput'] label"
    " { font-size:13px !important; color:#444 !important; }\n"  # noqa: E501
    "div[data-testid='stNumberInput'] input"
    " { border-radius:6px !important; font-size:14px !important; }\n"  # noqa: E501
    "div[data-testid='stAlert']"
    " { font-size:13px !important; padding:6px 12px !important;"
    " margin-top:2px !important; }\n"
    "div[data-testid='stSlider'] label"
    " { font-size:11px !important; color:#888 !important; }\n"
    "div[data-testid='stSlider'] [data-baseweb='slider']"
    " div[class*='Track'] > div:first-child"
    " { background:#119822 !important; }\n"
    "[data-testid='stSlider'] [data-baseweb='slider']"
    " [data-testid='stThumbValue'] { color:#119822 !important; }\n"  # noqa: E501
    "div[data-testid='stRadio'] [data-baseweb='radio']"
    " [role='radio']:checked ~ span { color: #119822 !important; }\n"  # noqa: E501
)
_IMPORT_URL = (  # noqa: E501
    "@import url('https://fonts.googleapis.com/css2?"
    "family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600"
    "&family=Outfit:wght@300;400;500;600&display=swap');\n"
)
# fmt: on

st.markdown(
    f"""
<style>
{_IMPORT_URL}
:root {{ --header-h: 72px; }}

body {{ background:#FFFFFF; font-family:'Outfit',sans-serif; }}
[data-testid="stSidebar"]        {{ display:none !important; }}
[data-testid="collapsedControl"] {{ display:none !important; }}

/* Hide Streamlit's own top bar */
[data-testid="stHeader"] {{ display:none !important; }}
#MainMenu {{ display:none !important; }}
footer    {{ display:none !important; }}

/* Push main content down so fixed navbar does not overlap it */
.main .block-container {{
    padding-top: calc(var(--header-h) + 1.5rem) !important;
}}

/* ── FIXED NAVBAR ── */
.custom-header {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: var(--header-h);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    background: #1a1a1a;
    box-shadow: 0 1px 4px rgba(0,0,0,.3);
    z-index: 1000;
}}
.navbar-brand {{ font-size:25px; font-weight:600; color:#fff; }}
.navbar-brand span {{ color:#119822; }}
.navbar-links {{ display:flex; align-items:center; gap:6px; }}
.navbar-links a {{
    color:rgba(255,255,255,0.55); text-decoration:none;
    font-size:12px; letter-spacing:0.08em;
    transition:color .2s;
}}
.navbar-links a:hover {{ color:#fff; }}
.nav-dot {{ color:#119822; margin:0 4px; opacity:.6; }}

/* HERO */
.hero-title {{
    font-size:48px; font-family:'Cormorant Garamond',serif;
    line-height:1.1; margin:20px 0 20px;
}}
.hero-desc  {{ font-size:18px; color:#555; margin-bottom:0; }}

/* CARD LABEL */
.card-label {{
    font-size:20px; letter-spacing:2px;
    text-transform:uppercase; color:#2A7221;
    font-weight:600; margin-bottom:0;
}}

/* SURVEY */
.matrix-title {{
    font-size:20px; font-weight:700;
    color:#1a1a1a; margin:6px 0 4px;
    padding-bottom:5px; border-bottom:2px solid #119822;
}}
.matrix-desc  {{
    font-size:16px; color:#666;
    margin-bottom:4px; line-height:1.5;
    margin-top:16px; }}
.criteria-name {{ font-size:14px; font-weight:600; color:#1a1a1a; }}

/* TOOLTIP */
.tooltip-wrap {{
    position: relative;
    display: inline-block;
    cursor: help;
    border-bottom: 1px dashed #119822;
}}
.tooltip-wrap .tooltip-box {{
    visibility: hidden;
    opacity: 0;
    width: 220px;
    background: #1a1a1a;
    color: #fff;
    font-size: 11px;
    font-weight: 400;
    line-height: 1.5;
    text-align: left;
    border-radius: 6px;
    padding: 8px 10px;
    position: absolute;
    z-index: 9999;
    bottom: 130%;
    left: 50%;
    transform: translateX(-50%);
    transition: opacity 0.2s;
    pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}}
.tooltip-wrap .tooltip-box::after {{
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border-width: 5px;
    border-style: solid;
    border-color: #1a1a1a transparent transparent transparent;
}}
.tooltip-wrap:hover .tooltip-box {{
    visibility: visible;
    opacity: 1;
}}

/* INPUTS */
{_CSS_LONG}
/* GREEN SLIDER */
div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {{
    background:#119822 !important;
    border-color:#119822 !important;
}}
div[data-testid="stSlider"] [data-baseweb="slider"] {{ --slider-color: #119822; }}

/* RADIO BUTTON */
div[data-testid="stRadio"] label {{ font-size:12px !important; }}
div[data-testid="stRadio"] {{ margin-top: 6px; }}

/* BUTTON */
.stButton > button {{
    background:#119822 !important; color:#fff !important;
    border:none !important; border-radius:6px !important;
    font-family:'Outfit',sans-serif !important; font-size:13px !important;
    font-weight:600 !important; padding:8px 20px !important;
    transition:background .2s !important;
}}
.stButton > button:hover    {{ background:#0d7a1b !important; }}
.stButton > button:disabled {{ opacity:0.4 !important; }}

/* Stepper buttons */
.step-btn > div > button {{
    border-radius:100px !important;
    font-size:12px !important;
    font-weight:600 !important;
    letter-spacing:0.03em !important;
    padding:6px 16px !important;
    width:auto !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- FIXED NAVBAR ----------
st.markdown(
    '<header class="custom-header">'
    '<div class="navbar-brand">Optimize<span>Saving</span></div>'
    '<nav class="navbar-links">'
    '<a href="#">TON THAT NHAT MINH</a><span class="nav-dot">&#183;</span>'
    '<a href="#">NGUYEN HOANG YEN NGOC</a>'
    '<span class="nav-dot">&#183;</span>'
    '<a href="#">NGUYEN THAO VY</a>'
    "</nav>"
    '<span style="font-size:10px;color:rgba(255,255,255,0.4);'
    'letter-spacing:0.04em;">'
    "Instructed by Dr. Dinh Hai Dung (VGU)"
    "</span>"
    "</div>"
    "</header>",
    unsafe_allow_html=True,
)


# ---------- HERO ----------
st.markdown(
    '<div class="hero-title">'
    "Make smarter <em>saving</em> decisions with data"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-desc">A two-stage framework combining '
    "<b>Monte Carlo simulation</b> with integrated approach "
    "<b>AHP-TOPSIS</b> — Complete your financial profile to unlock "
    "personalized insights.</div>",
    unsafe_allow_html=True,
)

st.divider()

# ---------- STEPPER ----------
STEPS = ["Savings Profile", "Criterias-Priority Survey", "Results"]
s0, sep1, s1, sep2, s2 = st.columns([2, 0.3, 2, 0.3, 1.5])

for col, idx, label in [
    (s0, 0, STEPS[0]),
    (s1, 1, STEPS[1]),
    (s2, 2, STEPS[2]),
]:
    with col:
        page = st.session_state.page
        if idx == page:
            st.markdown(
                f'<div style="display:inline-flex;align-items:center;'
                f"gap:8px;background:#119822;border-radius:100px;"
                f'padding:7px 16px;cursor:default;">'
                f'<span style="width:20px;height:20px;border-radius:50%;'
                f"background:rgba(255,255,255,0.2);display:flex;"
                f"align-items:center;justify-content:center;"
                f'font-size:11px;font-weight:700;color:#fff;">'
                f"{idx + 1}</span>"
                f'<span style="font-size:12px;font-weight:600;color:#fff;">'
                f"{label}</span></div>",
                unsafe_allow_html=True,
            )
        elif idx < page:
            if st.button(f"✓  {label}", key=f"step_btn_{idx}"):
                st.session_state.page = idx
                st.rerun()
        else:
            st.markdown(
                f'<div style="display:inline-flex;align-items:center;'
                f'gap:8px;padding:7px 4px;">'
                f'<span style="width:20px;height:20px;border-radius:50%;'
                f"background:#eee;display:flex;align-items:center;"
                f"justify-content:center;"
                f'font-size:11px;font-weight:700;color:#aaa;">'
                f"{idx + 1}</span>"
                f'<span style="font-size:12px;font-weight:600;color:#bbb;">'
                f"{label}</span></div>",
                unsafe_allow_html=True,
            )

for col, sep in [(sep1, ""), (sep2, "")]:
    with col:
        st.markdown(
            '<div style="height:34px;display:flex;align-items:center;">'
            '<div style="width:100%;height:1px;background:#ddd;"></div>'
            "</div>",
            unsafe_allow_html=True,
        )

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

# ================================================================
# PAGE 0 — SAVINGS PROFILE
# ================================================================
if st.session_state.page == 0:
    st.markdown(
        """
<div style="display:flex; align-items:center; gap:12px;">
    <div class="card-label">Your Savings Parameters</div>
    <div style="width:200px; height:1px; background:#2A7221;"></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        savings_target = st.number_input(
            "Savings Target (USD)",
            min_value=0,
            value=100_000_000,
            step=1_000_000,
            key="savings_target",
        )
    with col_b:
        time_horizon = st.number_input(
            "Time Horizon (months)",
            min_value=0,
            value=6,
            step=1,
            key="time_horizon",
        )
    with col_c:
        monthly_income = st.number_input(
            "Monthly Income - Gross (USD)",
            min_value=0,
            value=20_000_000,
            step=500_000,
            key="monthly_income",
        )

    col_d, col_e = st.columns(2)
    with col_d:
        monthly_spending = st.number_input(
            "Monthly Spending (USD)",
            min_value=0,
            value=9_000_000,
            step=100_000,
            key="monthly_spending",
        )
    with col_e:
        initial_wealth = st.number_input(
            "Initial Wealth (USD)",
            min_value=0,
            value=50_000_000,
            step=1_000_000,
            key="initial_wealth",
        )

    if savings_target == 0:
        st.warning("Savings Target cannot be 0.")
    if time_horizon == 0:
        st.warning("Time Horizon cannot be 0.")
    if monthly_income == 0:
        st.warning("Monthly Income cannot be 0.")
    if monthly_spending == 0:
        st.warning("Monthly Spending cannot be 0.")
    if initial_wealth == 0:
        st.warning("Initial Wealth cannot be 0.")
    if monthly_spending >= monthly_income:
        st.warning("Monthly Spending should be less than Monthly Income.")

    has_error = any(
        v == 0
        for v in [
            savings_target,
            time_horizon,
            monthly_income,
            monthly_spending,
            initial_wealth,
        ]
    )

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("NEXT →", disabled=has_error, key="save_btn"):
            st.session_state.page = 1
            st.rerun()


# ================================================================
# PAGE 1 — CRITERIAS-PRIORITY SURVEY
# ================================================================
elif st.session_state.page == 1:
    st.markdown(
        """
<div style="display:flex; align-items:center; gap:12px;">
    <div class="card-label">Criterias-Priority Survey</div>
    <div style="width:200px; height:1px; background:#2A7221;"></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="matrix-desc">'
        "Having in mind the goal: "
        "Select the criteria that you find more important and indicate "
        "how much more. "
        "If both criterions are equally important, select 1."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    SAATY_OPTIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    TOOLTIPS = {
        "Availability": "Can be purchased or invested in easily",
        "Information": ("Quality and transparency of data available about the option."),
        "Simplicity": "Full understanding of a financial product",
        "Stability": "Little or no danger of losing the investment",
        "Ability to save money": "Capacity to set aside money regularly",
        "Financial priorities": "Goals that guide where money is allocated",
        "Level of income": ("Overall earnings that determine saving potential"),
        "Liquidity": ("The ability to quickly convert the investment into cash"),
        "Return": "Dividends or interest to spend and/or reinvest",
        "Success rate": "Likelihood of achieving the target return",
        "Volatility": "The level of risk associated with price changes",
        "Experience": ("Prior hands-on engagement with financial instruments"),
        "Financial education": ("Knowledge of finance, investing, and economics"),
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
            "criteria": [
                "Availability",
                "Information",
                "Simplicity",
                "Stability",
            ],
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

    survey_results = {}

    def render_pairs(m, pairs, container):
        results = {}
        with container:
            for i, (a, b) in enumerate(pairs):
                radio_key = f"{m['key']}_{i}_side"
                scale_key = f"{m['key']}_{i}_scale"

                c_left, c_right = st.columns([0.5, 0.9], gap="small")

                with c_left:
                    tip_a = TOOLTIPS.get(a, "")
                    tip_b = TOOLTIPS.get(b, "")

                    def ttip(name, tip):
                        if tip:
                            return (
                                f'<span class="tooltip-wrap" '
                                f'style="font-size:14px;font-weight:600;'
                                f'color:#1a1a1a;">'
                                f"{name}"
                                f'<span class="tooltip-box">{tip}</span>'
                                f"</span>"
                            )
                        return (
                            f'<span style="font-size:14px;font-weight:600;'
                            f'color:#1a1a1a;">{name}</span>'
                        )

                    chosen = st.radio(
                        "prefer",
                        options=[a, b],
                        index=0,
                        key=radio_key,
                        label_visibility="collapsed",
                        horizontal=False,
                    )

                    _div_a = (
                        '<div style="height:12px;display:flex;'
                        'align-items:center;pointer-events:all;">'
                    )
                    _div_b = (
                        '<div style="height:42px;display:flex;'
                        'align-items:center;pointer-events:all;">'
                    )
                    _wrap = (
                        '<div style="position:relative;margin-top:-85px;'
                        'padding-left:50px;pointer-events:none;">'
                    )
                    st.markdown(
                        f"""
                        <style>
                        div[data-testid="stRadio"] p {{
                            color: transparent !important;
                            user-select: none;
                            pointer-events: none;
                        }}
                        div[data-testid="stRadio"] > div > label {{
                            align-items: center !important;
                            min-height: 35px !important;
                            padding: 4px 0 !important;
                        }}
                        </style>
                        {_wrap}
                          <div style="height:3px"></div>
                          {_div_a}
                            {ttip(a, tip_a)}
                          </div>
                          <div style="height:8px"></div>
                          {_div_b}
                            {ttip(b, tip_b)}
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with c_right:
                    st.markdown(
                        '<div style="height:10px"></div>',
                        unsafe_allow_html=True,
                    )
                    scale = st.select_slider(
                        "Intensity",
                        options=SAATY_OPTIONS,
                        value=1,
                        key=scale_key,
                        label_visibility="collapsed",
                        format_func=lambda x: str(x),
                    )

                if chosen == a:
                    value = float(scale)
                else:
                    value = 1.0 / float(scale) if scale != 0 else 1.0

                results[(a, b)] = value
        return results

    # --- Matrix 1: full width ---
    m = MATRICES[0]
    st.markdown(
        f'<div class="matrix-title">{m["title"]}</div>',
        unsafe_allow_html=True,
    )
    survey_results[m["key"]] = render_pairs(m, m["pairs"], st.container())

    st.divider()

    left_col, right_col = st.columns(2, gap="large")

    for m in [MATRICES[1], MATRICES[2]]:
        with left_col:
            st.markdown(
                f'<div class="matrix-title">{m["title"]}</div>',
                unsafe_allow_html=True,
            )
            survey_results[m["key"]] = render_pairs(m, m["pairs"], left_col)
            st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    for m in [MATRICES[3], MATRICES[4]]:
        with right_col:
            st.markdown(
                f'<div class="matrix-title">{m["title"]}</div>',
                unsafe_allow_html=True,
            )
            survey_results[m["key"]] = render_pairs(m, m["pairs"], right_col)
            st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        submit = st.button("LET'S SEE RESULTS →", key="survey_submit")

    if submit:
        all_matrices = {}
        for matrix in MATRICES:
            crit = matrix["criteria"]
            n = len(crit)
            idx = {c: i for i, c in enumerate(crit)}
            mat = np.ones((n, n))
            for (a, b), val in survey_results[matrix["key"]].items():
                i, j = idx[a], idx[b]
                mat[i][j] = val
                mat[j][i] = 1.0 / val if val != 0 else 1.0
            df = pd.DataFrame(mat, index=crit, columns=crit).round(3)
            all_matrices[matrix["key"]] = df

        st.session_state["ahp_matrices"] = all_matrices
        st.session_state.page = 2
        st.rerun()


# ================================================================
# PAGE 2 — RESULTS
# ================================================================
elif st.session_state.page == 2:
    st.markdown('<div class="card-label">Results</div>', unsafe_allow_html=True)
    st.success("Survey submitted! Pairwise matrices generated.")

    if "ahp_matrices" in st.session_state:
        MATRIX_TITLES = {
            "main": "Matrix 1: Main Criterias",
            "fin_sec": 'Matrix 2: Sub-criteria — "Financial Security"',
            "personal": ('Matrix 3: Sub-criteria — "Personal Characteristics"'),
            "profit": 'Matrix 4: Sub-criteria — "Profitability"',
            "readiness": 'Matrix 5: Sub-criteria — "Readiness"',
        }
        for key, title in MATRIX_TITLES.items():
            st.markdown(f"**{title}**")
            st.dataframe(
                st.session_state["ahp_matrices"][key],
                use_container_width=True,
            )
            st.markdown("")
