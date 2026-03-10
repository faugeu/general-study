import streamlit as st

# --- Page Setup ---
homepage = st.Page(
    page="pages/dashboard.py",
    title="Personal Finance Optimization",
)

ahp_page = st.Page(
    page="pages/investment_criterias.py",
    title="AHP Investment Analysis",
)

# --- Navigation ---
pg = st.navigation(pages=[homepage, ahp_page])

pg.run()
