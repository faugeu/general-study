import streamlit as st
from .constants import SAATY_OPTIONS
from .tooltip import tooltip_html


def render_pairs(matrix: dict, container) -> dict:
    """
    Render all pairwise-comparison rows for a single AHP matrix.

    Returns a dict  {(criterion_a, criterion_b): float value}
    where value > 1 means A is preferred, value < 1 means B is preferred.
    """
    results = {}
    pairs = matrix["pairs"]
    key_prefix = matrix["key"]

    with container:
        for i, (a, b) in enumerate(pairs):
            radio_key = f"{key_prefix}_{i}_side"
            scale_key = f"{key_prefix}_{i}_scale"

            c_left, c_right = st.columns([0.5, 0.9], gap="small")

            with c_left:
                chosen = st.radio(
                    "prefer",
                    options=[a, b],
                    index=0,
                    key=radio_key,
                    label_visibility="collapsed",
                    horizontal=False,
                )

                # Overlay styled labels on top of the invisible radio text
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
                      <div style="height:12px;display:flex;align-items:center;pointer-events:all;">
                        {tooltip_html(a)}
                      </div>
                      <div style="height:8px"></div>
                      <div style="height:42px;display:flex;align-items:center;pointer-events:all;">
                        {tooltip_html(b)}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with c_right:
                st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
                scale = st.select_slider(
                    "Intensity",
                    options=SAATY_OPTIONS,
                    value=1,
                    key=scale_key,
                    label_visibility="collapsed",
                    format_func=str,
                )

            value = (
                float(scale)
                if chosen == a
                else (1.0 / float(scale) if scale != 0 else 1.0)
            )
            results[(a, b)] = value

    return results


def render_matrix(matrix: dict, container) -> dict:
    """Render the title + pairs for one matrix block. Returns pair results."""
    with container:
        st.markdown(
            f'<div class="matrix-title">{matrix["title"]}</div>',
            unsafe_allow_html=True,
        )
    return render_pairs(matrix, container)
