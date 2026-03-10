import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

# ---------- CSS ----------
st.markdown(
    """
<style>

body {
    background:#FFFFFF;
    font-family: 'Outfit', sans-serif;
}

.logo {
    font-size:26px;
    font-weight:600;
}

.hero-title{
    font-size:48px;
    font-family:'Cormorant Garamond', serif;
}

.card{
    background:#F7F9F7;
    padding:24px;
    border:1px solid #E0E8E0;
    margin-bottom:20px;
}

.card-title{
    font-size:12px;
    letter-spacing:2px;
    text-transform:uppercase;
    color:#2A7221;
}

button[kind="primary"]{
    background:#119822;
}

</style>
""",
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
st.markdown(
    """
<div class="logo">Savings<span style="color:#119822">IQ</span></div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero-title">
Will you reach your <em>savings goal</em> in time?
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "Enter your financial target and spending habits to project the "
    "monthly success probability of three investment strategies."
)

st.divider()

# ---------- LAYOUT ----------
col_input, col_output = st.columns([1, 2])

# ---------- INPUT PANEL ----------
with col_input:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Financial Goal</div>', unsafe_allow_html=True)

    goal = st.number_input("Savings Target (₫)", value=100000000)
    period = st.number_input("Time Horizon (months)", value=24)
    income = st.number_input("Monthly Income (₫)", value=15000000)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-title">Spending Behaviour</div>', unsafe_allow_html=True
    )

    smin = st.number_input("Minimum Spending", value=5000000)
    savg = st.number_input("Average Spending", value=9000000)
    smax = st.number_input("Maximum Spending", value=13000000)

    st.markdown("</div>", unsafe_allow_html=True)

    run = st.button("Run Monte Carlo Simulation")


# ---------- MONTE CARLO ----------
def simulate(goal, T, income, smin, smax, r, v, N=5000):

    mr = r / 12
    mv = v / np.sqrt(12)

    success = np.zeros(T)

    for i in range(N):
        portfolio = 0

        for t in range(T):
            spend = np.random.uniform(smin, smax)
            save = max(0, income - spend)

            ret = np.random.normal(mr, mv)

            portfolio = portfolio * (1 + ret) + save

            if portfolio >= goal:
                success[t:] += 1
                break

    return success / N


# ---------- OUTPUT PANEL ----------
with col_output:

    if run:

        with st.spinner("Running Monte Carlo simulation..."):

            bank = simulate(goal, period, income, smin, smax, 0.055, 0.01)
            stock = simulate(goal, period, income, smin, smax, 0.15, 0.22)
            gold = simulate(goal, period, income, smin, smax, 0.08, 0.12)

        import pandas as pd

        df = pd.DataFrame(
            {
                "Month": np.arange(1, period + 1),
                "Bank Savings": bank,
                "Stock Investment": stock,
                "Gold Accumulation": gold,
            }
        )

        st.line_chart(df.set_index("Month"))

        final = {
            "Bank Savings": bank[-1],
            "Stock Investment": stock[-1],
            "Gold Accumulation": gold[-1],
        }

        best = max(final, key=final.get)
        worst = min(final, key=final.get)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("🏆 Optimal Strategy", best, f"{final[best]*100:.1f}%")

        with c2:
            st.metric("⚠️ Highest Risk", worst, f"{final[worst]*100:.1f}%")

        with c3:
            monthly = max(0, income - savg)
            st.metric("💰 Required Monthly Savings", f"{monthly:,.0f} ₫")
