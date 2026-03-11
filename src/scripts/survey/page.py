import streamlit as st
from .constants import MATRICES
from .matrix_widget import render_matrix
from .builder import build_ahp_matrices


def render_survey_page() -> None:
    """Render the full Criterias-Priority Survey page (page 1)."""
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

    survey_results = {}

    # Matrix 1 — full width
    survey_results[MATRICES[0]["key"]] = render_matrix(MATRICES[0], st.container())

    st.divider()

    # Matrices 2 & 3 on the left, 4 & 5 on the right
    left_col, right_col = st.columns(2, gap="large")

    for matrix in [MATRICES[1], MATRICES[2]]:
        survey_results[matrix["key"]] = render_matrix(matrix, left_col)
        left_col.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    for matrix in [MATRICES[3], MATRICES[4]]:
        survey_results[matrix["key"]] = render_matrix(matrix, right_col)
        right_col.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        submit = st.button("LET'S SEE RESULTS →", key="survey_submit")

    if submit:

        matrices = build_ahp_matrices(survey_results)

        # Check CI for all matrices
        invalid = []

        for name, result in matrices.items():
            if result["CR"] > 0.1:
                invalid.append(name)

        if invalid:
            st.error(
                "Your comparisons are inconsistent (CI > 0.1).\n\n"
                f"Please review the following matrices:\n\n" + ", ".join(invalid)
            )
            return

        st.session_state["ahp_matrices"] = matrices
        st.session_state.page = 2
        st.rerun()
