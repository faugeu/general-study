import streamlit as st
from savings_profile.page import render_profile_page
from survey.page import render_survey_page
from results.page import render_results_page

st.set_page_config(page_title="OptimizeSaving", page_icon="💰", layout="wide")

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = 0  # 0 = Savings Profile, 1 = Survey, 2 = Results

# ---------- CSS ----------
# fmt: off
_CSS_LONG = (
    "div[data-testid='stNumberInput'] label"
    " { font-size:13px !important; color:#444 !important; }\n"
    "div[data-testid='stNumberInput'] input"
    " { border-radius:6px !important; font-size:14px !important; }\n"
    "div[data-testid='stAlert']"
    " { font-size:13px !important; padding:6px 12px !important;"
    " margin-top:2px !important; }\n"
    "div[data-testid='stSlider'] label"
    " { font-size:11px !important; color:#888 !important; }\n"
    "div[data-testid='stSlider'] [data-baseweb='slider']"
    " div[class*='Track'] > div:first-child"
    " { background:#119822 !important; }\n"
    "[data-testid='stSlider'] [data-baseweb='slider']"
    " [data-testid='stThumbValue'] { color:#119822 !important; }\n"
    "div[data-testid='stRadio'] [data-baseweb='radio']"
    " [role='radio']:checked ~ span { color: #119822 !important; }\n"
)
_IMPORT_URL = (
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
[data-testid="stHeader"] {{ display:none !important; }}
#MainMenu {{ display:none !important; }}
footer    {{ display:none !important; }}

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
    font-size:12px; letter-spacing:0.08em; transition:color .2s;
}}
.navbar-links a:hover {{ color:#fff; }}
.nav-dot {{ color:#119822; margin:0 4px; opacity:.6; }}

/* HERO */
.hero-title {{
    font-size:48px; font-family:'Cormorant Garamond',serif;
    line-height:1.1; margin:20px 0 20px;
}}
.hero-desc {{ font-size:18px; color:#555; margin-bottom:0; }}

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
.matrix-desc {{
    font-size:16px; color:#666;
    margin-bottom:4px; line-height:1.5; margin-top:16px;
}}
.criteria-name {{ font-size:14px; font-weight:600; color:#1a1a1a; }}

/* TOOLTIP */
.tooltip-wrap {{
    position: relative; display: inline-block;
    cursor: help; border-bottom: 1px dashed #119822;
}}
.tooltip-wrap .tooltip-box {{
    visibility: hidden; opacity: 0; width: 220px;
    background: #1a1a1a; color: #fff;
    font-size: 11px; font-weight: 400; line-height: 1.5;
    text-align: left; border-radius: 6px; padding: 8px 10px;
    position: absolute; z-index: 9999;
    bottom: 130%; left: 50%; transform: translateX(-50%);
    transition: opacity 0.2s; pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}}
.tooltip-wrap .tooltip-box::after {{
    content: ""; position: absolute; top: 100%; left: 50%;
    transform: translateX(-50%); border-width: 5px; border-style: solid;
    border-color: #1a1a1a transparent transparent transparent;
}}
.tooltip-wrap:hover .tooltip-box {{ visibility: visible; opacity: 1; }}

/* INPUTS */
{_CSS_LONG}
div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {{
    background:#119822 !important; border-color:#119822 !important;
}}
div[data-testid="stSlider"] [data-baseweb="slider"] {{ --slider-color: #119822; }}
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

.step-btn > div > button {{
    border-radius:100px !important; font-size:12px !important;
    font-weight:600 !important; letter-spacing:0.03em !important;
    padding:6px 16px !important; width:auto !important;
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
    '<span style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:0.04em;">'
    "Instructed by Dr. Dinh Hai Dung (VGU)"
    "</span>"
    "</div>"
    "</header>",
    unsafe_allow_html=True,
)

# ---------- HERO ----------
st.markdown(
    '<div class="hero-title">Make smarter <em>saving</em> decisions with data</div>',
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

for col, idx, label in [(s0, 0, STEPS[0]), (s1, 1, STEPS[1]), (s2, 2, STEPS[2])]:
    with col:
        page = st.session_state.page
        if idx == page:
            st.markdown(
                f'<div style="display:inline-flex;align-items:center;gap:8px;'
                f'background:#119822;border-radius:100px;padding:7px 16px;cursor:default;">'
                f'<span style="width:20px;height:20px;border-radius:50%;'
                f"background:rgba(255,255,255,0.2);display:flex;align-items:center;"
                f'justify-content:center;font-size:11px;font-weight:700;color:#fff;">'
                f"{idx + 1}</span>"
                f'<span style="font-size:12px;font-weight:600;color:#fff;">{label}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )
        elif idx < page:
            if st.button(f"✓  {label}", key=f"step_btn_{idx}"):
                st.session_state.page = idx
                st.rerun()
        else:
            st.markdown(
                f'<div style="display:inline-flex;align-items:center;gap:8px;padding:7px 4px;">'
                f'<span style="width:20px;height:20px;border-radius:50%;background:#eee;'
                f"display:flex;align-items:center;justify-content:center;"
                f'font-size:11px;font-weight:700;color:#aaa;">{idx + 1}</span>'
                f'<span style="font-size:12px;font-weight:600;color:#bbb;">{label}</span>'
                f"</div>",
                unsafe_allow_html=True,
            )

for col in [sep1, sep2]:
    with col:
        st.markdown(
            '<div style="height:34px;display:flex;align-items:center;">'
            '<div style="width:100%;height:1px;background:#ddd;"></div>'
            "</div>",
            unsafe_allow_html=True,
        )

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

# ---------- PAGE DISPATCH ----------
if st.session_state.page == 0:
    render_profile_page()
elif st.session_state.page == 1:
    render_survey_page()
elif st.session_state.page == 2:
    render_results_page()
