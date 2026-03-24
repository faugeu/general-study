import streamlit as st
from .constants import MATRICES, MATRIX_EXPLANATIONS
from .matrix_widget import render_matrix
from .builder import build_ahp_matrices


def render_explanation(matrix_key: str):
    """Render explanation box for example mode."""
    if not st.session_state.get("is_example", False):
        return

    explanation = MATRIX_EXPLANATIONS.get(matrix_key)
    if not explanation:
        return

    with st.expander(f"💡 {explanation['title']}", expanded=False):
        st.markdown(explanation["text"])


# ---------- MAIN PAGE ----------
def render_survey_page() -> None:
    """Render the full Criterias-Priority Survey page (page 1)."""

    # Header
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

    # ---------- MATRIX 1 (FULL WIDTH) ----------
    with st.container():
        render_explanation(MATRICES[0]["key"])  # ✅ explanation
        survey_results[MATRICES[0]["key"]] = render_matrix(MATRICES[0], st.container())

    st.divider()

    # ---------- TWO-COLUMN LAYOUT ----------
    left_col, right_col = st.columns(2, gap="large")

    # Left column (Matrices 2 & 3)
    for matrix in [MATRICES[1], MATRICES[2]]:
        with left_col:
            render_explanation(matrix["key"])  # ✅ explanation
            survey_results[matrix["key"]] = render_matrix(matrix, left_col)
            st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # Right column (Matrices 4 & 5)
    for matrix in [MATRICES[3], MATRICES[4]]:
        with right_col:
            render_explanation(matrix["key"])  # ✅ explanation
            survey_results[matrix["key"]] = render_matrix(matrix, right_col)
            st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    # ---------- SUBMIT BUTTON ----------
    _, btn_col, _ = st.columns([3, 2, 3])
    with btn_col:
        submit = st.button("LET'S SEE RESULTS →", key="survey_submit")

    # ---------- VALIDATION + NEXT STEP ----------
    if submit:

        matrices = build_ahp_matrices(survey_results)

        invalid = []
        for name, result in matrices.items():
            if result["CR"] > 0.1:
                invalid.append(name)

        if invalid:
            st.error(
                "Your comparisons are inconsistent (CR > 0.1).\n\n"
                f"Please review the following matrices:\n\n" + ", ".join(invalid)
            )
            return

        st.session_state["ahp_matrices"] = matrices
        # st.session_state["is_example"] = False
        st.session_state.page = 2
        st.rerun()
