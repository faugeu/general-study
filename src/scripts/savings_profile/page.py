import streamlit as st
from .inputs import render_inputs
from .validation import validate


def render_profile_page() -> None:
    """Render the full Savings Profile page (page 0)."""
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

    values = render_inputs()
    has_error = validate(values)

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        if st.button("NEXT →", disabled=has_error, key="save_btn"):
            # Save values under separate keys (prefixed with "profile_") to
            # avoid the StreamlitAPIException that occurs when trying to write
            # to a session_state key already owned by an active widget.
            # results/page.py reads from these "profile_*" keys.
            for field, value in values.items():
                st.session_state[f"profile_{field}"] = value

            # Invalidate any cached Monte Carlo results so the simulation
            # reruns with the new parameters on the Results page.
            st.session_state.pop("mc_results", None)

            st.session_state.page = 1
            st.rerun()
