import streamlit as st
from .inputs import render_inputs
from .validation import validate


def render_profile_page() -> None:
    """Render the full Savings Profile page (page 0)."""

    # ── Show example mode banner ──
    if st.session_state.get("is_example") and not st.session_state.get(
        "profile_viewed_once"
    ):
        st.markdown(
            '<div style="'
            "background:rgba(17,152,34,0.12);"
            "border:1px solid #119822;"
            "border-radius:8px;"
            "padding:12px 18px;"
            "margin-bottom:18px;"
            "font-size:13px;"
            'color:var(--text-color);">'
            "<b>Example Mode</b> — The savings profile below is prefilled with "
            "<b>Minh's financial data</b>. You can modify any values or "
            "proceed as-is to the survey."
            "</div>",
            unsafe_allow_html=True,
        )
        # Mark that user has seen the profile page
        st.session_state["profile_viewed_once"] = True

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

    values = render_inputs()  # This will automatically use prefilled values
    has_error = validate(values)

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("NEXT →", disabled=has_error, key="save_btn"):
            # Save values under separate keys
            for field, value in values.items():
                st.session_state[f"profile_{field}"] = value

            # Invalidate cached Monte Carlo results
            st.session_state.pop("mc_results", None)

            st.session_state.page = 1
            st.rerun()
